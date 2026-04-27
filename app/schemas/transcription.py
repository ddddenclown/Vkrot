from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from app.models.transcription import TranscriptionStatus


class TranscribeRequest(BaseModel):
    s3_url: str
    language: Optional[str] = None


class WordSchema(BaseModel):
    word: str
    start: float
    end: float
    confidence: Optional[float] = None

    class Config:
        from_attributes = True


class TranscriptionResponse(BaseModel):
    id: str
    status: TranscriptionStatus
    language: Optional[str] = None
    words: List[WordSchema] = []

    class Config:
        from_attributes = True


class TranscriptionStatusResponse(BaseModel):
    id: str
    status: TranscriptionStatus

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    error: bool = True
    message: str
    code: int
