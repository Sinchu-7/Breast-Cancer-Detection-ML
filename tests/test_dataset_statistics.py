
import pytest

from src.dataset_statistics import generate_dataset_statistics
from src.prepare_image_dataset import CLASSES, MAGNIFICATIONS


def create_sample_dataset(root):
    """Create a small BreakHis-style dataset for testing."""

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:
            folder = root / magnification / class_name
            folder.mkdir(parents=True)

            filename = (
                f"patient_{class_name}_{magnification}"
                f"-{magnification.replace('X', '')}-001.png"
            )

            (folder / filename).write_bytes(b"sample image")


def test_dataset_statistics_counts(tmp_path):
    create_sample_dataset(tmp_path)

    statistics = generate_dataset_statistics(tmp_path)

    assert statistics["total_images"] == 8
    assert statistics["total_patients"] == 8

    assert statistics["class_distribution"] == {
        "benign": 4,
        "malignant": 4,
    }

    assert statistics["magnification_distribution"] == {
        "40X": 2,
        "100X": 2,
        "200X": 2,
        "400X": 2,
    }


def test_dataset_statistics_percentages(tmp_path):
    create_sample_dataset(tmp_path)

    statistics = generate_dataset_statistics(tmp_path)

    assert statistics["class_percentages"] == {
        "benign": 50.0,
        "malignant": 50.0,
    }

    assert statistics["magnification_percentages"] == {
        "40X": 25.0,
        "100X": 25.0,
        "200X": 25.0,
        "400X": 25.0,
    }


def test_missing_dataset_directory(tmp_path):
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        generate_dataset_statistics(missing_directory)


def test_missing_dataset_folder(tmp_path):
    create_sample_dataset(tmp_path)

    missing_folder = tmp_path / "400X" / "malignant"
    
    for image in missing_folder.iterdir():
        image.unlink()

    missing_folder.rmdir()

    with pytest.raises(FileNotFoundError):
        generate_dataset_statistics(tmp_path)


def test_empty_dataset_folder(tmp_path):
    create_sample_dataset(tmp_path)

    empty_folder = tmp_path / "400X" / "malignant"

    for image in empty_folder.iterdir():
        image.unlink()

    with pytest.raises(ValueError):
        generate_dataset_statistics(tmp_path)
