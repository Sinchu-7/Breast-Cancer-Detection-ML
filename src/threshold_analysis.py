
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)


THRESHOLDS = np.arange(0.20, 0.81, 0.05)


def analyze_thresholds(true_labels, probabilities):

    true_labels = np.asarray(true_labels).astype(int)
    probabilities = np.asarray(probabilities).reshape(-1)

    if len(true_labels) != len(probabilities):
        raise ValueError(
            "Labels and probabilities must have the same length."
        )

    if len(true_labels) == 0:
        raise ValueError("Input data cannot be empty.")

    if not np.isin(true_labels, [0, 1]).all():
        raise ValueError("Labels must contain only 0 and 1.")

    if not np.isfinite(probabilities).all():
        raise ValueError("Probabilities must be finite.")

    if np.any((probabilities < 0) | (probabilities > 1)):
        raise ValueError("Probabilities must be between 0 and 1.")

    results = []

    for threshold in THRESHOLDS:

        predictions = (
            probabilities >= threshold
        ).astype(int)

        tn, fp, fn, tp = confusion_matrix(
            true_labels,
            predictions,
            labels=[0, 1],
        ).ravel()

        result = {
            "threshold": round(float(threshold), 2),
            "accuracy": round(
                float(accuracy_score(true_labels, predictions)) * 100, 2
            ),
            "precision": round(
                float(precision_score(
                    true_labels,
                    predictions,
                    zero_division=0,
                )) * 100, 2
            ),
            "recall": round(
                float(recall_score(
                    true_labels,
                    predictions,
                    zero_division=0,
                )) * 100, 2
            ),
            "f1_score": round(
                float(f1_score(
                    true_labels,
                    predictions,
                    zero_division=0,
                )) * 100, 2
            ),
            "false_negatives": int(fn),
            "confusion_matrix": [
                [int(tn), int(fp)],
                [int(fn), int(tp)],
            ],
        }

        results.append(result)

    return results


def main():

    validation_path = Path("data/image_splits/validation.json")
    model_path = Path("models/breast_histopathology_mobilenetv2.keras")
    report_path = Path("reports/threshold_analysis.json")

    if not validation_path.exists():
        raise FileNotFoundError(validation_path)

    if not model_path.exists():
        raise FileNotFoundError(model_path)

    import tensorflow as tf
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

    from src.compare_image_models import load_image_data

    with open(validation_path, "r", encoding="utf-8") as file:
        validation_data = json.load(file)

    images, labels = load_image_data(validation_data)

    model = tf.keras.models.load_model(model_path)

    probabilities = model.predict(
        images,
        batch_size=32,
        verbose=1,
    ).reshape(-1)

    results = analyze_thresholds(labels, probabilities)

    print("\n" + "=" * 85)
    print("CLASSIFICATION THRESHOLD ANALYSIS")
    print("=" * 85)

    print(
        f"{'Threshold':<13}"
        f"{'Accuracy':<13}"
        f"{'Precision':<13}"
        f"{'Recall':<13}"
        f"{'F1-score':<13}"
        f"{'FN':<8}"
    )

    print("-" * 85)

    for result in results:
        print(
            f"{result['threshold']:<13.2f}"
            f"{result['accuracy']:<13.2f}"
            f"{result['precision']:<13.2f}"
            f"{result['recall']:<13.2f}"
            f"{result['f1_score']:<13.2f}"
            f"{result['false_negatives']:<8}"
        )

    best_f1 = max(results, key=lambda item: item["f1_score"])

    print("\nBest F1-score threshold:", best_f1["threshold"])
    print("Best F1-score:", best_f1["f1_score"])

    report_path.parent.mkdir(parents=True, exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print("\nReport saved to:", report_path)


if __name__ == "__main__":
    main()
