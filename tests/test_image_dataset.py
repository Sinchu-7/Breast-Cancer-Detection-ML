
import pytest

from src.prepare_image_dataset import (
    CLASSES,
    MAGNIFICATIONS,
    get_patient_id,
    validate_dataset_structure,
    validate_splits,
)

from src.dataset_config import DatasetSplitConfig


def create_dataset_structure(root):
    """Create a temporary dataset with sample image files."""

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:
            folder = root / magnification / class_name
            folder.mkdir(parents=True)
            (folder / "sample.png").touch()


# Dataset structure tests

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


# Patient ID extraction tests

@pytest.mark.parametrize(
    "filename",
    [
        "SOB_B_A-40-001.png",
        "SOB_B_A-100-001.png",
        "SOB_B_A-200-001.png",
        "SOB_B_A-400-001.png",
    ],
)
def test_patient_id_extraction_across_magnifications(filename):
    assert get_patient_id(filename) == "SOB_B_A"


def test_patient_id_without_magnification_suffix():
    assert get_patient_id("SOB_B_A.png") == "SOB_B_A"


# Dataset split configuration tests

def test_default_split_configuration():
    config = DatasetSplitConfig()

    assert config.n_splits == 5
    assert config.random_state == 42


def test_custom_split_configuration():
    config = DatasetSplitConfig(n_splits=4, random_state=123)

    assert config.n_splits == 4
    assert config.random_state == 123


def test_invalid_split_count():
    with pytest.raises(ValueError):
        DatasetSplitConfig(n_splits=1)


def test_negative_random_state():
    with pytest.raises(ValueError):
        DatasetSplitConfig(random_state=-1)


# Dataset split validation tests

def test_valid_dataset_splits():
    all_paths = [
        "40X/benign/SOB_B_A-40-001.png",
        "40X/malignant/SOB_M_A-40-001.png",
        "100X/benign/SOB_B_B-100-001.png",
    ]

    all_groups = [
        "SOB_B_A",
        "SOB_M_A",
        "SOB_B_B",
    ]

    splits = {
        "train": [all_paths[0]],
        "validation": [all_paths[1]],
        "test": [all_paths[2]],
    }

    patient_sets = validate_splits(splits, all_paths, all_groups)

    assert len(patient_sets) == 3


def test_empty_split_rejected():
    all_paths = ["40X/benign/SOB_B_A-40-001.png"]

    splits = {
        "train": all_paths,
        "validation": [],
        "test": [],
    }

    with pytest.raises(ValueError, match="empty"):
        validate_splits(splits, all_paths, ["SOB_B_A"])


def test_duplicate_images_rejected():
    path = "40X/benign/SOB_B_A-40-001.png"

    splits = {
        "train": [path],
        "validation": [path],
        "test": ["40X/benign/SOB_B_B-40-001.png"],
    }

    with pytest.raises(ValueError, match="Duplicate"):
        validate_splits(
            splits,
            [path, "40X/benign/SOB_B_B-40-001.png"],
            ["SOB_B_A", "SOB_B_B"],
        )


def test_missing_images_rejected():
    all_paths = [
        "40X/benign/SOB_B_A-40-001.png",
        "40X/benign/SOB_B_B-40-001.png",
        "40X/malignant/SOB_M_A-40-001.png",
        "40X/malignant/SOB_M_B-40-001.png",
    ]

    splits = {
        "train": [all_paths[0]],
        "validation": [all_paths[1]],
        "test": [all_paths[2]],
    }

    with pytest.raises(ValueError, match="missing or extra"):
        validate_splits(splits, all_paths, ["A", "B", "C", "D"])


def test_patient_leakage_rejected():
    path_a = "40X/benign/SOB_B_A-40-001.png"
    path_b = "100X/benign/SOB_B_A-100-002.png"
    path_c = "40X/malignant/SOB_M_B-40-001.png"

    all_paths = [path_a, path_b, path_c]

    splits = {
        "train": [path_a],
        "validation": [path_b],
        "test": [path_c],
    }

    with pytest.raises(ValueError, match="Patient leakage"):
        validate_splits(
            splits,
            all_paths,
            ["SOB_B_A", "SOB_B_A", "SOB_M_B"],
        )


def test_missing_split_name_rejected():
    all_paths = ["40X/benign/SOB_B_A-40-001.png"]

    splits = {
        "train": all_paths,
        "validation": [],
    }

    with pytest.raises(ValueError, match="must contain"):
        validate_splits(splits, all_paths, ["SOB_B_A"])
