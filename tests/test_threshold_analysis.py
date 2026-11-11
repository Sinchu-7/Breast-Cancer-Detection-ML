
import numpy as np
import pytest

from src.threshold_analysis import analyze_thresholds


def test_threshold_analysis_returns_all_thresholds():

    labels = np.array([0, 0, 1, 1, 1])
    probabilities = np.array([0.1, 0.4, 0.6, 0.8, 0.9])

    results = analyze_thresholds(labels, probabilities)

    assert len(results) == 13


def test_threshold_analysis_contains_required_metrics():

    labels = np.array([0, 0, 1, 1])
    probabilities = np.array([0.1, 0.3, 0.7, 0.9])

    results = analyze_thresholds(labels, probabilities)

    required_fields = {
        "threshold",
        "accuracy",
        "precision",
        "recall",
        "f1_score",
        "false_negatives",
        "confusion_matrix",
    }

    for result in results:
        assert required_fields.issubset(result.keys())


def test_lower_threshold_does_not_increase_false_negatives():

    labels = np.array([0, 1, 1, 1, 0])
    probabilities = np.array([0.2, 0.3, 0.6, 0.8, 0.7])

    results = analyze_thresholds(labels, probabilities)

    false_negatives = [
        result["false_negatives"]
        for result in results
    ]

    # As the threshold increases, false negatives cannot decrease.
    assert all(
        false_negatives[i] <= false_negatives[i + 1]
        for i in range(len(false_negatives) - 1)
    )


def test_threshold_analysis_confusion_matrix():

    labels = np.array([0, 0, 1, 1])
    probabilities = np.array([0.1, 0.8, 0.4, 0.9])

    results = analyze_thresholds(labels, probabilities)

    result = next(
        item for item in results
        if item["threshold"] == 0.5
    )

    assert result["confusion_matrix"] == [
        [1, 1],
        [1, 1],
    ]


def test_threshold_analysis_rejects_fractional_labels():

    labels = np.array([0, 0.8, 1])
    probabilities = np.array([0.1, 0.5, 0.9])

    with pytest.raises(
        ValueError,
        match="Labels must contain only 0 and 1",
    ):
        analyze_thresholds(labels, probabilities)
