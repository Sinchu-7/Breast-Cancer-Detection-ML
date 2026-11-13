
from pathlib import Path

import numpy as np
from PIL import Image


# Project configuration
PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "breast_histopathology_mobilenetv2.keras"
)

IMAGE_SIZE = (224, 224)

CLASS_NAMES = ["Benign", "Malignant"]

# Selected using validation data only
CLASSIFICATION_THRESHOLD = 0.30


def preprocess_image(image):
    """
    Prepare an uploaded image for MobileNetV2 prediction.
    """
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    image = image.convert("RGB")
    image = image.resize(IMAGE_SIZE)

    image_array = np.array(
        image,
        dtype=np.float32
    )

    image_array = preprocess_input(image_array)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    return image_array


def predict_image(image, model, threshold=CLASSIFICATION_THRESHOLD):
    """
    Predict whether an image belongs to the benign or malignant class.

    The threshold is applied to the model's malignant-class output score.
    """

    if not 0 <= threshold <= 1:
        raise ValueError("Threshold must be between 0 and 1.")

    image_array = preprocess_image(image)

    prediction = model.predict(
        image_array,
        verbose=0
    )

    malignant_score = float(
        np.asarray(prediction).reshape(-1)[0]
    )

    if not np.isfinite(malignant_score):
        raise ValueError("Model returned an invalid prediction score.")

    if not 0 <= malignant_score <= 1:
        raise ValueError("Model output must be between 0 and 1.")

    if malignant_score >= threshold:
        predicted_class = "Malignant"
        confidence = malignant_score * 100
    else:
        predicted_class = "Benign"
        confidence = (1 - malignant_score) * 100

    return predicted_class, confidence, malignant_score
