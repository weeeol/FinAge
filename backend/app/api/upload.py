from fastapi import APIRouter, UploadFile, File, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.upload import UploadResponse
from app.services.import_service import ImportService

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.post("", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_statement(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()
    service = ImportService(db)
    return service.process_upload(content=content, filename=file.filename or "statement.csv")
