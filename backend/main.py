from functools import lru_cache
from io import BytesIO

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError
from starlette.concurrency import run_in_threadpool

from src.predict import CLASSIFICATION_THRESHOLD, IMAGE_SIZE, MODEL_PATH


MAX_UPLOAD_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG"}

app = FastAPI(
    title="Histology Research API",
    description="Educational image-classification research prototype.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@lru_cache(maxsize=1)
def load_model():
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    import tensorflow as tf

    return tf.keras.models.load_model(MODEL_PATH)


def decode_image(data: bytes) -> Image.Image:
    if not data:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        with Image.open(BytesIO(data)) as image:
            if image.format not in ALLOWED_IMAGE_FORMATS:
                raise HTTPException(
                    status_code=415,
                    detail="Upload a PNG or JPEG histopathology image.",
                )
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise HTTPException(
                    status_code=413,
                    detail="The image dimensions exceed the 25-megapixel limit.",
                )
            image.load()
            return image.convert("RGB")
    except UnidentifiedImageError as error:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid PNG or JPEG image.",
        ) from error
    except (OSError, Image.DecompressionBombError) as error:
        raise HTTPException(
            status_code=400,
            detail="The image could not be decoded.",
        ) from error


def run_prediction(image: Image.Image) -> tuple[str, float, float]:
    model = load_model()
    from src.predict import predict_image

    return predict_image(image, model, CLASSIFICATION_THRESHOLD)


@app.get("/api/health")
def health():
    model_available = MODEL_PATH.is_file()
    return {
        "status": "ready" if model_available else "model_unavailable",
        "model_available": model_available,
    }


@app.get("/api/model")
def model_details():
    return {
        "architecture": "MobileNetV2",
        "input_size": list(IMAGE_SIZE),
        "classes": ["Benign", "Malignant"],
        "classification_threshold": CLASSIFICATION_THRESHOLD,
        "dataset": "BreakHis",
        "purpose": "Educational research only",
    }


@app.post("/api/predict")
async def predict(file: UploadFile = File(...)):
    data = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=413,
            detail="The file is larger than the 10 MB upload limit.",
        )

    image = decode_image(data)

    try:
        predicted_class, confidence, malignant_score = await run_in_threadpool(
            run_prediction,
            image,
        )
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail="The trained model is unavailable. Add the model file to models/.",
        ) from error

    return {
        "predicted_class": predicted_class,
        "confidence_percent": round(confidence, 2),
        "malignant_score_percent": round(malignant_score * 100, 2),
        "threshold": CLASSIFICATION_THRESHOLD,
        "disclaimer": "Experimental output only; not a medical diagnosis.",
    }
