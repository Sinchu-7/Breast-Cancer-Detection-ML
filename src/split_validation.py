
import json
from pathlib import Path


# ============================================================
# SPLIT JSON VALIDATION
# ============================================================

REQUIRED_FIELDS = {
    "path",
    "label",
    "class",
    "patient_id"
}

VALID_CLASSES = {
    "benign": 0,
    "malignant": 1
}


def validate_split_records(records):
    """Validate the structure and contents of split records."""

    if not isinstance(records, list):
        raise ValueError("Split JSON must contain a list of records.")

    if not records:
        raise ValueError("Split JSON contains no records.")

    seen_paths = set()

    for index, record in enumerate(records):

        if not isinstance(record, dict):
            raise ValueError(
                f"Record {index} must be a dictionary."
            )

        missing_fields = REQUIRED_FIELDS - set(record.keys())

        if missing_fields:
            raise ValueError(
                f"Record {index} is missing fields: "
                f"{sorted(missing_fields)}"
            )

        image_path = record["path"]
        label = record["label"]
        class_name = record["class"]
        patient_id = record["patient_id"]

        if not isinstance(image_path, str) or not image_path.strip():
            raise ValueError(
                f"Record {index} has an invalid image path."
            )

        normalized_path = str(
            Path(image_path).resolve()
        ).casefold()

        if normalized_path in seen_paths:
            raise ValueError(
                f"Duplicate image path found: {image_path}"
            )

        seen_paths.add(normalized_path)

        if not isinstance(class_name, str):
            raise ValueError(
                f"Record {index} has an invalid class."
            )

        if class_name not in VALID_CLASSES:
            raise ValueError(
                f"Record {index} has unknown class: {class_name}"
            )

        if isinstance(label, bool) or not isinstance(label, int):
            raise ValueError(
                f"Record {index} has an invalid label."
            )

        expected_label = VALID_CLASSES[class_name]

        if label != expected_label:
            raise ValueError(
                f"Label mismatch in record {index}: "
                f"{class_name} must have label {expected_label}."
            )

        if (
            not isinstance(patient_id, str)
            or not patient_id.strip()
            or patient_id != patient_id.strip()
        ):
            raise ValueError(
                f"Record {index} has an invalid patient ID."
            )

    return True


def load_split_records(split_path):
    """Load a JSON split file and validate its records."""

    path = Path(split_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"Split file not found: {path}"
        )

    try:
        with open(path, "r", encoding="utf-8") as file:
            records = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(
            f"Invalid JSON in split file: {path}"
        ) from error

    validate_split_records(records)

    return records


def validate_all_split_files(split_dir="data/image_splits"):
    """Validate train, validation, and test JSON files."""

    directory = Path(split_dir)

    if not directory.is_dir():
        raise FileNotFoundError(
            f"Split directory not found: {directory}"
        )

    split_names = [
        "train",
        "validation",
        "test"
    ]

    all_records = {}
    all_paths = set()

    print("\n========== SPLIT JSON VALIDATION ==========")

    for split_name in split_names:

        split_path = directory / f"{split_name}.json"

        records = load_split_records(split_path)

        current_paths = {
            str(Path(record["path"]).resolve()).casefold()
            for record in records
        }

        overlap = all_paths & current_paths

        if overlap:
            raise ValueError(
                f"Duplicate image paths found across split files: "
                f"{split_name}"
            )

        all_paths.update(current_paths)

        all_records[split_name] = records

        print(
            f"{split_name.capitalize()}: "
            f"{len(records)} valid records"
        )

    # Check patient leakage between split files.
    patient_sets = {
        split_name: {
            record["patient_id"]
            for record in records
        }
        for split_name, records in all_records.items()
    }

    split_names = list(patient_sets.keys())

    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):

            first = split_names[i]
            second = split_names[j]

            overlap = (
                patient_sets[first]
                & patient_sets[second]
            )

            if overlap:
                raise ValueError(
                    f"Patient leakage between {first} and {second}: "
                    f"{sorted(overlap)}"
                )

    print("\nAll split JSON files passed validation.")

    return all_records


if __name__ == "__main__":
    validate_all_split_files()
