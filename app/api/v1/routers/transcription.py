from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
import tempfile, shutil
from app.schemas.transcription import TranscribeRequest, TranscriptionResponse, TranscriptionStatusResponse
from app.crud import transcription as crud
from app.services.pipeline import run_transcription_pipeline, run_transcription_pipeline_from_file
from app.db import get_db
from app.core.security import verify_basic_auth

router = APIRouter()


@router.post("/transcriptions", response_model=TranscriptionStatusResponse, status_code=202)
async def create_transcription(
    data: TranscribeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: str = Depends(verify_basic_auth),
):
    t = crud.create_transcription(db, data)
    background_tasks.add_task(run_transcription_pipeline, db, t.id, data.s3_url, data.language)
    return t


@router.post("/transcriptions/upload", response_model=TranscriptionStatusResponse, status_code=202)
async def upload_transcription(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    _: str = Depends(verify_basic_auth),
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
):
    suffix = "." + (file.filename.rsplit(".", 1)[-1] if "." in file.filename else "m4a")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    shutil.copyfileobj(file.file, tmp)
    tmp.close()

    from app.schemas.transcription import TranscribeRequest
    t = crud.create_transcription(db, TranscribeRequest(s3_url=f"file://{tmp.name}", language=language))
    background_tasks.add_task(run_transcription_pipeline_from_file, db, t.id, tmp.name, language)
    return t


@router.get("/transcriptions/{transcription_id}", response_model=TranscriptionResponse)
def get_transcription(
    transcription_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(verify_basic_auth),
):
    t = crud.get_transcription(db, transcription_id)
    if not t:
        raise HTTPException(status_code=404, detail="Not found")
    return t
