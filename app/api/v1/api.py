from fastapi import APIRouter
from app.api.v1.routers import transcription

router = APIRouter()
router.include_router(transcription.router, tags=["transcription"])
