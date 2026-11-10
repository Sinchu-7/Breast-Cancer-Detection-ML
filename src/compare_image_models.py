
import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# ============================================================
# CONFIGURATION
# ============================================================

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16

VALIDATION_JSON = "data/image_splits/validation.json"

MODELS = {
    "baseline": (
        "models/breast_histopathology_mobilenetv2.keras"
    ),
    "finetuned": (
        "models/breast_histopathology_mobilenetv2_finetuned.keras"
    ),
}

OUTPUT_PATH = "reports/validation_model_comparison.json"


# ============================================================
# LOAD VALIDATION DATA
# ============================================================

def load_validation_data(json_path):

    with open(json_path, "r", encoding="utf-8") as file:
        records = json.load(file)

    paths = [record["path"] for record in records]
    labels = np.array(
        [record["label"] for record in records]
    )

    if not paths:
        raise ValueError("Validation dataset is empty.")

    if len(paths) != len(labels):
        raise ValueError("Validation paths and labels do not match.")

    print("Validation images:", len(paths))

    return paths, labels


# ============================================================
# IMAGE PREPROCESSING
# ============================================================

def preprocess_image(filepath):

    image = tf.io.read_file(filepath)

    image = tf.io.decode_image(
        image,
        channels=3,
        expand_animations=False,
    )

    image = tf.image.resize(image, IMAGE_SIZE)
    image = preprocess_input(image)

    return image


def create_validation_dataset(paths):

    dataset = tf.data.Dataset.from_tensor_slices(paths)

    dataset = dataset.map(
        preprocess_image,
        num_parallel_calls=tf.data.AUTOTUNE,
    )

    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    return dataset


# ============================================================
# EVALUATE MODEL
# ============================================================

def evaluate_model(model_name, model_path, dataset, true_labels):

    if not os.path.isfile(model_path):
        raise FileNotFoundError(
            f"Model not found: {model_path}"
        )

    print(f"\nEvaluating {model_name} model...")

    model = tf.keras.models.load_model(
        model_path,
        compile=False,
    )

    probabilities = model.predict(
        dataset,
        verbose=1,
    ).flatten()

    if len(probabilities) != len(true_labels):
        raise ValueError(
            "Prediction count does not match validation labels."
        )

    if not np.all(np.isfinite(probabilities)):
        raise ValueError(
            "Model generated invalid prediction probabilities."
        )

    if np.any(probabilities < 0) or np.any(probabilities > 1):
        raise ValueError(
            "Predictions are outside the expected probability range."
        )

    predicted_labels = (
        probabilities >= 0.5
    ).astype(int)

    results = {
        "accuracy": float(
            accuracy_score(true_labels, predicted_labels)
        ),
        "precision": float(
            precision_score(
                true_labels,
                predicted_labels,
                zero_division=0,
            )
        ),
        "recall": float(
            recall_score(
                true_labels,
                predicted_labels,
                zero_division=0,
            )
        ),
        "f1_score": float(
            f1_score(
                true_labels,
                predicted_labels,
                zero_division=0,
            )
        ),
        "roc_auc": float(
            roc_auc_score(true_labels, probabilities)
        ),
        "confusion_matrix": confusion_matrix(
            true_labels,
            predicted_labels,
            labels=[0, 1],
        ).tolist(),
        "classification_report": classification_report(
            true_labels,
            predicted_labels,
            labels=[0, 1],
            target_names=["Benign", "Malignant"],
            zero_division=0,
            output_dict=True,
        ),
    }

    del model

    return results


# ============================================================
# DISPLAY COMPARISON
# ============================================================

def print_comparison(results):

    print("\n" + "=" * 65)
    print("MOBILENETV2 VALIDATION MODEL COMPARISON")
    print("=" * 65)

    metrics = [
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
    ]

    print(
        f"\n{'Metric':<15}"
        f"{'Baseline':<18}"
        f"{'Fine-tuned':<18}"
    )

    print("-" * 51)

    for metric in metrics:

        baseline = results["baseline"][metric] * 100
        finetuned = results["finetuned"][metric] * 100

        print(
            f"{metric.capitalize():<15}"
            f"{baseline:<18.2f}"
            f"{finetuned:<18.2f}"
        )

    print("\nBaseline Confusion Matrix:")
    print(results["baseline"]["confusion_matrix"])

    print("\nFine-tuned Confusion Matrix:")
    print(results["finetuned"]["confusion_matrix"])

    print("\n" + "=" * 65)


# ============================================================
# MAIN
# ============================================================

def main():

    paths, true_labels = load_validation_data(
        VALIDATION_JSON
    )

    validation_dataset = create_validation_dataset(paths)

    results = {
        "validation_images": len(paths),
        "baseline": evaluate_model(
            "baseline",
            MODELS["baseline"],
            validation_dataset,
            true_labels,
        ),
        "finetuned": evaluate_model(
            "finetuned",
            MODELS["finetuned"],
            validation_dataset,
            true_labels,
        ),
    }

    print_comparison(results)

    os.makedirs("reports", exist_ok=True)

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            results,
            file,
            indent=4,
        )

    print("\nComparison saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    main()
