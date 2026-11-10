
import numpy as np

from src.data_preprocessing import load_data, preprocess_data


def test_load_data():
    X, y = load_data()

    assert X.shape == (569, 30)
    assert y.shape == (569,)
    assert set(np.unique(y)) == {0, 1}


def test_preprocessing_shapes():
    X, y = load_data()

    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)

    assert X_train.shape[0] == 455
    assert X_test.shape[0] == 114
    assert X_train.shape[1] == 30
    assert X_test.shape[1] == 30


def test_scaled_training_data():
    X, y = load_data()

    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)

    assert np.allclose(X_train.mean(axis=0), 0, atol=1e-7)
    assert np.allclose(X_train.std(axis=0), 1, atol=1e-7)


def test_stratified_split():
    X, y = load_data()

    X_train, X_test, y_train, y_test, scaler = preprocess_data(X, y)

    original_ratio = np.mean(y)
    train_ratio = np.mean(y_train)
    test_ratio = np.mean(y_test)

    assert abs(original_ratio - train_ratio) < 0.02
    assert abs(original_ratio - test_ratio) < 0.02


def test_reproducible_split():
    X, y = load_data()

    first = preprocess_data(X, y, random_state=42)
    second = preprocess_data(X, y, random_state=42)

    assert np.array_equal(first[0], second[0])
    assert np.array_equal(first[1], second[1])
