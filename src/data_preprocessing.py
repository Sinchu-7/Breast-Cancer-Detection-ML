
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data():
    """Load the Wisconsin Breast Cancer dataset."""
    dataset = load_breast_cancer()
    return dataset.data, dataset.target


def preprocess_data(X, y, test_size=0.2, random_state=42):
    """Split data and scale features without data leakage."""

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return (
        X_train_scaled,
        X_test_scaled,
        y_train,
        y_test,
        scaler
    )


def main():
    X, y = load_data()

    print("Original Dataset Shape:", X.shape)

    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)

    print("\nTraining Samples:", X_train.shape[0])
    print("Testing Samples:", X_test.shape[0])

    print("\nPreprocessing Completed!")
    print("Scaled Training Shape:", X_train.shape)
    print("Scaled Testing Shape:", X_test.shape)

    print("\nFirst 5 scaled training records:")
    print(X_train[:5])


if __name__ == "__main__":
    main()
