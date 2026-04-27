from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.db import Base


class TranscriptionStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    done = "done"
    failed = "failed"


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(String, primary_key=True)
    s3_url = Column(String, nullable=False)
    status = Column(Enum(TranscriptionStatus), default=TranscriptionStatus.pending)
    language = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    words = relationship("Word", back_populates="transcription", cascade="all, delete-orphan")


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transcription_id = Column(String, ForeignKey("transcriptions.id"), nullable=False)
    word = Column(String, nullable=False)
    start = Column(Float, nullable=False)
    end = Column(Float, nullable=False)
    confidence = Column(Float, nullable=True)

    transcription = relationship("Transcription", back_populates="words")
