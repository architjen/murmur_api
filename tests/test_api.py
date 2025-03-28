from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


def test_ping():
    response = client.get("/hello")
    print(response)
    assert response.status_code == 200


def test_transcribe_endpoint():
    with open("tests/test_audio.wav", "rb") as audio_file:
        response = client.post("/transcribe", files={"file": audio_file})
    print(response)
    assert response.status_code == 200
    assert "text" in response.json()
