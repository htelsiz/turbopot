from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_generate_content():
    response = client.post(
        "/generate_content",
        json={"prompt": "Test prompt", "content_type": "general", "voice": "alloy", "high_quality": False}
    )
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "audio/mpeg"
    assert "Content-Disposition" in response.headers
    assert response.headers["Content-Disposition"] == "attachment; filename=generated_content.mp3"

def test_generate_content_invalid_input():
    response = client.post(
        "/generate_content",
        json={"prompt": "", "content_type": "invalid_type", "voice": "invalid_voice", "high_quality": "not_a_boolean"}
    )
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.parametrize("content_type", ["blog", "poem", "story"])
def test_generate_content_different_types(content_type):
    response = client.post(
        "/generate_content",
        json={"prompt": f"Test {content_type}", "content_type": content_type, "voice": "alloy", "high_quality": False}
    )
    assert response.status_code == 200

def test_generate_content_high_quality():
    response = client.post(
        "/generate_content",
        json={"prompt": "Test high quality", "content_type": "general", "voice": "alloy", "high_quality": True}
    )
    assert response.status_code == 200
