from io import BytesIO

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from PIL import Image

from backend import main
from backend.main import app, decode_image

client = TestClient(app)


def image_bytes(image_format="PNG"):
    buffer = BytesIO()
    Image.new("RGB", (4, 3), color=(120, 130, 140)).save(
        buffer,
        format=image_format,
    )
    return buffer.getvalue()


def test_decode_image_returns_rgb_image():
    image = decode_image(image_bytes())

    assert image.mode == "RGB"
    assert image.size == (4, 3)


@pytest.mark.parametrize(
    ("data", "status_code"),
    [
        (b"", 400),
        (b"not an image", 400),
        (image_bytes("GIF"), 415),
    ],
)
def test_decode_image_rejects_invalid_or_unsupported_images(data, status_code):
    with pytest.raises(HTTPException) as error:
        decode_image(data)

    assert error.value.status_code == status_code


def test_health_endpoint_reports_model_availability(monkeypatch, tmp_path):
    monkeypatch.setattr(main, "MODEL_PATH", tmp_path / "missing.keras")

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "model_unavailable",
        "model_available": False,
    }


def test_model_endpoint_returns_model_metadata():
    response = client.get("/api/model")

    assert response.status_code == 200
    assert response.json()["input_size"] == [224, 224]
    assert response.json()["classes"] == ["Benign", "Malignant"]


def test_predict_endpoint_returns_prediction(monkeypatch):
    monkeypatch.setattr(main, "load_model", lambda: object())
    monkeypatch.setattr(
        "src.predict.predict_image",
        lambda image, model, threshold: ("Malignant", 85.0, 0.85),
        raising=False,
    )

    response = client.post(
        "/api/predict",
        files={"file": ("sample.png", image_bytes(), "image/png")},
    )

    assert response.status_code == 200
    assert response.json()["predicted_class"] == "Malignant"
    assert response.json()["confidence_percent"] == 85.0
    assert response.json()["malignant_score_percent"] == 85.0
