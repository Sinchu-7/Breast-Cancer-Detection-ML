
import json
import pytest

from src.split_validation import (
    validate_split_records,
    load_split_records,
    validate_all_split_files,
)


def create_valid_record(
    path="image1.png",
    label=0,
    class_name="benign",
    patient_id="patient1",
):
    return {
        "path": path,
        "label": label,
        "class": class_name,
        "patient_id": patient_id,
    }


# ============================================================
# RECORD VALIDATION TESTS
# ============================================================

def test_valid_split_records():
    records = [
        create_valid_record(),
        create_valid_record(
            path="image2.png",
            label=1,
            class_name="malignant",
            patient_id="patient2",
        ),
    ]

    assert validate_split_records(records) is True


def test_empty_records():
    with pytest.raises(ValueError, match="no records"):
        validate_split_records([])


def test_records_must_be_a_list():
    with pytest.raises(ValueError, match="must contain a list"):
        validate_split_records({"path": "image.png"})


def test_missing_required_field():
    record = create_valid_record()
    del record["patient_id"]

    with pytest.raises(ValueError, match="missing fields"):
        validate_split_records([record])


def test_invalid_record_type():
    with pytest.raises(ValueError, match="must be a dictionary"):
        validate_split_records(["invalid"])


def test_empty_image_path():
    record = create_valid_record(path=" ")

    with pytest.raises(ValueError, match="invalid image path"):
        validate_split_records([record])


def test_duplicate_image_paths():
    records = [
        create_valid_record(path="image.png"),
        create_valid_record(path="image.png"),
    ]

    with pytest.raises(ValueError, match="Duplicate image path"):
        validate_split_records(records)


def test_unknown_class():
    record = create_valid_record(class_name="unknown")

    with pytest.raises(ValueError, match="unknown class"):
        validate_split_records([record])


def test_invalid_label():
    record = create_valid_record(label=2)

    with pytest.raises(ValueError, match="Label mismatch"):
        validate_split_records([record])


def test_boolean_label_is_rejected():
    record = create_valid_record(label=True)

    with pytest.raises(ValueError, match="invalid label"):
        validate_split_records([record])


def test_label_class_mismatch():
    record = create_valid_record(
        label=0,
        class_name="malignant",
    )

    with pytest.raises(ValueError, match="Label mismatch"):
        validate_split_records([record])


def test_empty_patient_id():
    record = create_valid_record(patient_id=" ")

    with pytest.raises(ValueError, match="invalid patient ID"):
        validate_split_records([record])


# ============================================================
# JSON FILE LOADING TESTS
# ============================================================

def test_load_valid_json_file(tmp_path):
    records = [create_valid_record()]

    json_file = tmp_path / "train.json"
    json_file.write_text(
        json.dumps(records),
        encoding="utf-8",
    )

    loaded_records = load_split_records(json_file)

    assert loaded_records == records


def test_missing_json_file(tmp_path):
    json_file = tmp_path / "missing.json"

    with pytest.raises(FileNotFoundError, match="Split file not found"):
        load_split_records(json_file)


def test_invalid_json_file(tmp_path):
    json_file = tmp_path / "invalid.json"
    json_file.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_split_records(json_file)


# ============================================================
# ALL SPLIT FILES TESTS
# ============================================================

def create_split_files(directory):
    directory.mkdir(parents=True, exist_ok=True)

    split_data = {
        "train": [
            create_valid_record(
                path="train.png",
                patient_id="patient1",
            )
        ],
        "validation": [
            create_valid_record(
                path="validation.png",
                label=1,
                class_name="malignant",
                patient_id="patient2",
            )
        ],
        "test": [
            create_valid_record(
                path="test.png",
                patient_id="patient3",
            )
        ],
    }

    for split_name, records in split_data.items():
        file_path = directory / f"{split_name}.json"

        file_path.write_text(
            json.dumps(records),
            encoding="utf-8",
        )


def test_validate_all_split_files(tmp_path):
    create_split_files(tmp_path)

    result = validate_all_split_files(tmp_path)

    assert len(result["train"]) == 1
    assert len(result["validation"]) == 1
    assert len(result["test"]) == 1


def test_missing_split_directory(tmp_path):
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError, match="Split directory not found"):
        validate_all_split_files(missing_directory)


def test_patient_leakage_between_splits(tmp_path):
    create_split_files(tmp_path)

    validation_file = tmp_path / "validation.json"

    records = json.loads(
        validation_file.read_text(encoding="utf-8")
    )

    records[0]["patient_id"] = "patient1"

    validation_file.write_text(
        json.dumps(records),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Patient leakage"):
        validate_all_split_files(tmp_path)


def test_duplicate_paths_across_splits(tmp_path):
    create_split_files(tmp_path)

    validation_file = tmp_path / "validation.json"

    records = json.loads(
        validation_file.read_text(encoding="utf-8")
    )

    records[0]["path"] = "train.png"

    validation_file.write_text(
        json.dumps(records),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Duplicate image paths"):
        validate_all_split_files(tmp_path)
