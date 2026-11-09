
import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# -------------------------------
# CONFIGURATION
# -------------------------------

MODEL_PATH = "models/breast_histopathology_mobilenetv2_finetuned.keras"
TEST_JSON = "data/image_splits/test.json"

IMAGE_SIZE = (224, 224)

CLASS_NAMES = ["Benign", "Malignant"]


# -------------------------------
# LOAD TEST DATA
# -------------------------------

with open(TEST_JSON, "r", encoding="utf-8") as file:
    records = json.load(file)

test_paths = [record["path"] for record in records]
true_labels = np.array([record["label"] for record in records])

print("Test images:", len(test_paths))


# -------------------------------
# LOAD TRAINED MODEL
# -------------------------------

print("\nLoading trained model...")

model = tf.keras.models.load_model(MODEL_PATH)

print("Model loaded successfully!")


# -------------------------------
# PREPROCESS TEST IMAGES
# -------------------------------

def preprocess_image(filepath):
    image = tf.io.read_file(filepath)

    image = tf.io.decode_png(
        image,
        channels=3
    )

    image = tf.image.resize(
        image,
        IMAGE_SIZE
    )

    image = preprocess_input(image)

    return image


# -------------------------------
# MAKE PREDICTIONS
# -------------------------------

print("\nPredicting test images...")

predictions = []

for i in range(0, len(test_paths), 16):
    batch_paths = test_paths[i:i + 16]

    batch_images = [
        preprocess_image(path)
        for path in batch_paths
    ]

    batch_images = tf.stack(batch_images)

    batch_predictions = model.predict(
        batch_images,
        verbose=0
    )

    predictions.extend(batch_predictions.flatten())

probabilities = np.array(predictions)

predicted_labels = (
    probabilities >= 0.5
).astype(int)


# -------------------------------
# EVALUATION METRICS
# -------------------------------

accuracy = accuracy_score(
    true_labels,
    predicted_labels
)

precision = precision_score(
    true_labels,
    predicted_labels,
    zero_division=0
)

recall = recall_score(
    true_labels,
    predicted_labels,
    zero_division=0
)

f1 = f1_score(
    true_labels,
    predicted_labels,
    zero_division=0
)

cm = confusion_matrix(
    true_labels,
    predicted_labels
)


# -------------------------------
# DISPLAY RESULTS
# -------------------------------

print("\n" + "=" * 50)
print("BREAST HISTOPATHOLOGY MODEL EVALUATION")
print("=" * 50)

print(f"\nAccuracy:  {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall:    {recall * 100:.2f}%")
print(f"F1-score:  {f1 * 100:.2f}%")

print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")

print(
    classification_report(
        true_labels,
        predicted_labels,
        labels=[0, 1],
        target_names=CLASS_NAMES,
        zero_division=0
    )
)


# -------------------------------
# SAVE EVALUATION RESULTS
# -------------------------------

os.makedirs("reports", exist_ok=True)

results = {
    "accuracy": float(accuracy),
    "precision": float(precision),
    "recall": float(recall),
    "f1_score": float(f1),
    "confusion_matrix": cm.tolist(),
    "test_images": len(test_paths)
}

with open(
    "reports/image_model_evaluation.json",
    "w",
    encoding="utf-8"
) as file:
    json.dump(results, file, indent=4)

print("\nEvaluation saved to:")
print("reports/image_model_evaluation.json")
