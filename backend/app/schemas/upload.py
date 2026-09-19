from typing import List
from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    imported: int = Field(..., description="Number of transactions successfully imported")
    skipped: int = Field(0, description="Number of duplicate or unparseable transactions skipped")
    categories_assigned: int = Field(0, description="Number of transactions mapped to a specific category")
    warnings: List[str] = Field(default_factory=list, description="Warnings encountered during file processing")
