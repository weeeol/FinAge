import os
from typing import Tuple, Dict
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from app.core.config import settings
from app.schemas.upload import UploadResponse
from app.processing.parser import parse_statement_file
from app.models.category import Category
from app.models.transaction import Transaction


class ImportService:
    def __init__(self, db: Session):
        self.db = db

    def process_upload(self, content: bytes, filename: str, user_id: int = 1) -> UploadResponse:
        # 1. Validation checks
        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded file is empty."
            )

        if len(content) > settings.UPLOAD_MAX_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds maximum allowed size of {settings.UPLOAD_MAX_SIZE_BYTES // (1024 * 1024)}MB."
            )

        ext = os.path.splitext(filename)[1].lower()
        if ext not in settings.ALLOWED_UPLOAD_EXTENSIONS:
            raise HTTPException(
                status_code=422,
                detail=f"Unsupported file format '{ext}'. FinAge accepts .csv, .xlsx, or .pdf files."
            )

        # 2. Parse file content
        try:
            candidates, warnings = parse_statement_file(content, filename)
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error parsing statement: {str(e)}"
            )

        if not candidates and not warnings:
            return UploadResponse(
                imported=0,
                skipped=0,
                categories_assigned=0,
                warnings=["File contains no recognizable transactions."]
            )

        # 3. Load categories from database
        categories = self.db.execute(select(Category)).scalars().all()
        cat_map: Dict[str, Category] = {c.name.lower(): c for c in categories}
        other_cat = cat_map.get("other")

        # 4. Query existing transactions for duplicate detection
        existing_txns = self.db.execute(
            select(Transaction.transaction_date, Transaction.description, Transaction.amount_minor)
            .filter_by(user_id=user_id)
        ).all()
        existing_set = set(existing_txns)

        imported_count = 0
        skipped_count = len(warnings)  # Row parsing errors are counted as skipped
        categories_assigned_count = 0

        new_entities = []

        for item in candidates:
            # Duplicate check
            key = (item.transaction_date, item.description, item.amount_minor)
            if key in existing_set:
                skipped_count += 1
                warnings.append(f"Skipped duplicate transaction: {item.transaction_date} - {item.description} ({item.amount_minor / 100:.2f})")
                continue

            existing_set.add(key)  # Prevent duplicates within the same upload

            # Resolve Category ID
            cat_name = (item.category_name or "Other").lower()
            matched_cat = cat_map.get(cat_name, other_cat)
            cat_id = matched_cat.id if matched_cat else None

            if matched_cat and matched_cat.name != "Other":
                categories_assigned_count += 1

            # Build model
            txn = Transaction(
                user_id=user_id,
                category_id=cat_id,
                transaction_date=item.transaction_date,
                description=item.description,
                amount_minor=item.amount_minor,
                currency=item.currency,
                source_file=filename,
                is_recurring_candidate=False,
            )
            new_entities.append(txn)
            imported_count += 1

        if new_entities:
            self.db.add_all(new_entities)
            self.db.commit()

        return UploadResponse(
            imported=imported_count,
            skipped=skipped_count,
            categories_assigned=categories_assigned_count,
            warnings=warnings,
        )
