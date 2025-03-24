from pydantic import BaseModel
from typing import Optional
from fastapi import UploadFile

class DocumentIn(BaseModel):
    title: str
    content: Optional[str] = None  # Optional if file is provided
    file: Optional[UploadFile] = None  # For file uploads

class QuestionIn(BaseModel):
    question: str