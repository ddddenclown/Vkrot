import whisperx
import torch
from typing import List, Dict
from app.core.config import settings


def get_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def transcribe(wav_path: str, language: str = None) -> List[Dict]:
    device = get_device()
    compute_type = "float16" if device == "cuda" else "int8"

    model = whisperx.load_model(
        settings.WHISPER_MODEL,
        device,
        compute_type=compute_type,
        language=language,
    )

    audio = whisperx.load_audio(wav_path)
    result = model.transcribe(audio, batch_size=settings.WHISPER_BATCH_SIZE)

    align_model, metadata = whisperx.load_align_model(
        language_code=result["language"],
        device=device,
    )
    result = whisperx.align(
        result["segments"],
        align_model,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    words = []
    for segment in result["segments"]:
        for w in segment.get("words", []):
            words.append({
                "word": w["word"].strip(),
                "start": w.get("start", 0.0),
                "end": w.get("end", 0.0),
                "confidence": w.get("score"),
            })

    return words
