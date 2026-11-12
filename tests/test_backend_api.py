from io import BytesIO

import pytest
from fastapi import HTTPException
from PIL import Image

from backend.main import decode_image


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
