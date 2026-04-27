from sqlalchemy.orm import Session
from app.models.transcription import Transcription, Word, TranscriptionStatus
from app.schemas.transcription import TranscribeRequest
from typing import Optional, List
import uuid


def create_transcription(db: Session, data: TranscribeRequest) -> Transcription:
    t = Transcription(
        id=str(uuid.uuid4()),
        s3_url=data.s3_url,
        language=data.language,
        status=TranscriptionStatus.pending,
    )
    db.add(t)
    db.commit()
    db.refresh(t)
    return t


def get_transcription(db: Session, transcription_id: str) -> Optional[Transcription]:
    return db.query(Transcription).filter(Transcription.id == transcription_id).first()


def update_status(db: Session, transcription_id: str, status: TranscriptionStatus) -> Optional[Transcription]:
    t = get_transcription(db, transcription_id)
    if t:
        t.status = status
        db.commit()
        db.refresh(t)
    return t


def save_words(db: Session, transcription_id: str, words: List[dict]) -> None:
    db.query(Word).filter(Word.transcription_id == transcription_id).delete()
    for w in words:
        db.add(Word(
            transcription_id=transcription_id,
            word=w["word"],
            start=w["start"],
            end=w["end"],
            confidence=w.get("confidence"),
        ))
    db.commit()
