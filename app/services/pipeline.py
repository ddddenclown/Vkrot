from sqlalchemy.orm import Session
from app.crud import transcription as crud
from app.models.transcription import TranscriptionStatus
from app.services.audio import download_from_presigned_url, convert_to_wav, cleanup
from app.services.transcription import transcribe


async def run_transcription_pipeline(db: Session, transcription_id: str, s3_url: str, language: str = None):
    crud.update_status(db, transcription_id, TranscriptionStatus.processing)
    wav_path = None
    try:
        m4a_path = await download_from_presigned_url(s3_url)
        wav_path = convert_to_wav(m4a_path)
        words = transcribe(wav_path, language=language)
        crud.save_words(db, transcription_id, words)
        crud.update_status(db, transcription_id, TranscriptionStatus.done)
    except Exception as e:
        crud.update_status(db, transcription_id, TranscriptionStatus.failed)
        raise e
    finally:
        if wav_path:
            cleanup(wav_path)


async def run_transcription_pipeline_from_file(db: Session, transcription_id: str, file_path: str, language: str = None):
    crud.update_status(db, transcription_id, TranscriptionStatus.processing)
    wav_path = None
    try:
        wav_path = convert_to_wav(file_path)
        words = transcribe(wav_path, language=language)
        crud.save_words(db, transcription_id, words)
        crud.update_status(db, transcription_id, TranscriptionStatus.done)
    except Exception as e:
        crud.update_status(db, transcription_id, TranscriptionStatus.failed)
        raise e
    finally:
        if wav_path:
            cleanup(wav_path)

