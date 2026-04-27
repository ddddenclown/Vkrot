FROM python:3.11-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir numpy"<2" && \
    pip install --no-cache-dir torch torchaudio --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir whisperx && \
    pip install --no-cache-dir fastapi==0.111.0 "uvicorn[standard]==0.29.0" sqlalchemy==2.0.30 pydantic-settings==2.2.1 httpx==0.27.0 jiwer==3.0.4 pytest==8.2.0 pytest-asyncio==0.23.6

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
