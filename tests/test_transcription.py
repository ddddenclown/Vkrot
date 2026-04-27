import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings
import base64

client = TestClient(app)


def auth_header():
    token = base64.b64encode(f"{settings.API_USERNAME}:{settings.API_PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def test_create_transcription():
    r = client.post(
        "/api/v1/transcriptions",
        json={"s3_url": "https://example.com/vocal.m4a"},
        headers=auth_header(),
    )
    assert r.status_code == 202
    data = r.json()
    assert "id" in data
    assert data["status"] == "pending"


def test_get_transcription_not_found():
    r = client.get("/api/v1/transcriptions/nonexistent", headers=auth_header())
    assert r.status_code == 404


def test_unauthorized():
    r = client.post("/api/v1/transcriptions", json={"s3_url": "https://example.com/vocal.m4a"})
    assert r.status_code == 401
