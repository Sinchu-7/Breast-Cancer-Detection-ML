import pytest

from src.prepare_image_dataset import (
    CLASSES,
    MAGNIFICATIONS,
    validate_dataset_structure,
)


def create_dataset_structure(root):
    """Create a temporary dataset with sample image files."""

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:
            folder = root / magnification / class_name
            folder.mkdir(parents=True)

            # Create a sample image file for validation
            (folder / "sample.png").touch()


def test_valid_dataset_structure(tmp_path):
    create_dataset_structure(tmp_path)

    total_images = validate_dataset_structure(tmp_path)

    assert total_images == 8


def test_missing_dataset_folder(tmp_path):
    create_dataset_structure(tmp_path)

    missing_folder = tmp_path / "40X" / "benign"
    (missing_folder / "sample.png").unlink()
    missing_folder.rmdir()

    with pytest.raises(FileNotFoundError):
        validate_dataset_structure(tmp_path)


def test_empty_dataset_folder(tmp_path):
    create_dataset_structure(tmp_path)

    empty_folder = tmp_path / "40X" / "benign"
    (empty_folder / "sample.png").unlink()

    with pytest.raises(ValueError):
        validate_dataset_structure(tmp_path)


def test_unsupported_image_extension(tmp_path):
    create_dataset_structure(tmp_path)

    folder = tmp_path / "40X" / "benign"
    (folder / "sample.png").unlink()
    (folder / "sample.txt").touch()

    with pytest.raises(ValueError):
        validate_dataset_structure(tmp_path)