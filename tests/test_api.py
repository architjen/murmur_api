from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    print(app.router.routes)
    assert response.status_code == 200


def test_ping():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello world"}


def test_transcribe_endpoint():
    with open("tests/test_audio.wav", "rb") as audio_file:
        response = client.post("/transcribe", files={"file": audio_file})
    assert response.status_code == 200
    assert "text" in response.json()


def test_invalid_transcribe_endpoint():
    response = client.post("/transcribe", files={"file": "not_an_audio"})
    assert response.status_code != 200
