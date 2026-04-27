import httpx
import tempfile
import os
import subprocess
from pathlib import Path


async def download_from_presigned_url(url: str) -> str:
    suffix = ".m4a"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.get(url)
        r.raise_for_status()
        tmp.write(r.content)
    tmp.close()
    return tmp.name


def convert_to_wav(input_path: str) -> str:
    output_path = input_path.replace(".m4a", ".wav")
    subprocess.run(
        ["ffmpeg", "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
        check=True,
        capture_output=True,
    )
    os.unlink(input_path)
    return output_path


def cleanup(path: str) -> None:
    try:
        os.unlink(path)
    except FileNotFoundError:
        pass
