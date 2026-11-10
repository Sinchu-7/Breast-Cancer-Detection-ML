
import os
import re
import json
from pathlib import Path

from sklearn.model_selection import StratifiedGroupKFold

# Dataset location
DATASET_DIR = (
    r"C:\Users\sinch\Downloads\BreakHis - Breast Cancer Histopathological Database"
    r"\BreakHis - Breast Cancer Histopathological Database"
    r"\images\dataset_cancer_v1\classificacao_binaria"
)

OUTPUT_DIR = "data/image_splits"

CLASSES = ["benign", "malignant"]
MAGNIFICATIONS = ["40X", "100X", "200X", "400X"]

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff"}


def validate_dataset_structure(dataset_dir=DATASET_DIR):
    """Validate dataset folders and image availability."""

    root = Path(dataset_dir)

    if not root.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {root}"
        )

    total_images = 0

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:
            folder = root / magnification / class_name

            if not folder.is_dir():
                raise FileNotFoundError(
                    f"Required dataset folder is missing: {folder}"
                )

            images = [
                file for file in folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in SUPPORTED_EXTENSIONS
            ]

            if not images:
                raise ValueError(
                    f"No supported images found in: {folder}"
                )

            total_images += len(images)

            print(
                f"Validated {magnification}/{class_name}: "
                f"{len(images)} images"
            )

    print(f"\nDataset validation successful: {total_images} images.")

    return total_images


def get_patient_id(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]

    return re.sub(
        r"-(40|100|200|400)-\d+$",
        "",
        filename
    )


def collect_images(dataset_dir=DATASET_DIR):
    """Collect image paths, labels and patient groups."""

    paths = []
    labels = []
    groups = []

    validate_dataset_structure(dataset_dir)

    root = Path(dataset_dir)

    for label, class_name in enumerate(CLASSES):
        for magnification in MAGNIFICATIONS:

            folder = root / magnification / class_name

            files = sorted(
                file for file in folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in SUPPORTED_EXTENSIONS
            )

            for filepath in files:
                paths.append(str(filepath.resolve()))
                labels.append(label)
                groups.append(get_patient_id(filepath))

    normalized_paths = [
        os.path.normcase(os.path.realpath(path))
        for path in paths
    ]

    if len(normalized_paths) != len(set(normalized_paths)):
        raise ValueError("Duplicate image paths detected.")

    if not paths:
        raise ValueError("No images were collected.")

    if len(paths) != len(labels) or len(paths) != len(groups):
        raise ValueError("Image paths, labels and groups are inconsistent.")

    return paths, labels, groups


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    paths, labels, groups = collect_images()

    print("\nTotal images:", len(paths))
    print("Unique patients:", len(set(groups)))

    # First split: 80% development, 20% test
    splitter = StratifiedGroupKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    train_val_idx, test_idx = next(
        splitter.split(paths, labels, groups)
    )

    # Second split: 80% train, 20% validation
    train_val_paths = [paths[i] for i in train_val_idx]
    train_val_labels = [labels[i] for i in train_val_idx]
    train_val_groups = [groups[i] for i in train_val_idx]

    second_splitter = StratifiedGroupKFold(
        n_splits=5,
        shuffle=True,
        random_state=42
    )

    train_idx, val_idx = next(
        second_splitter.split(
            train_val_paths,
            train_val_labels,
            train_val_groups
        )
    )

    splits = {
        "train": [train_val_paths[i] for i in train_idx],
        "validation": [train_val_paths[i] for i in val_idx],
        "test": [paths[i] for i in test_idx],
    }

    # Verify no patient appears in multiple splits
    patient_sets = {
        name: {get_patient_id(path) for path in files}
        for name, files in splits.items()
    }

    assert patient_sets["train"].isdisjoint(patient_sets["validation"])
    assert patient_sets["train"].isdisjoint(patient_sets["test"])
    assert patient_sets["validation"].isdisjoint(patient_sets["test"])

    # Save split information
    for split_name, files in splits.items():
        records = []

        for filepath in files:
            class_name = os.path.basename(os.path.dirname(filepath))

            records.append({
                "path": filepath,
                "label": CLASSES.index(class_name),
                "class": class_name,
                "patient_id": get_patient_id(filepath)
            })

        output_path = os.path.join(
            OUTPUT_DIR, f"{split_name}.json"
        )

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)

        print(f"\n{split_name.upper()}")
        print("Images:", len(records))
        print(
            "Benign:",
            sum(r["class"] == "benign" for r in records)
        )
        print(
            "Malignant:",
            sum(r["class"] == "malignant" for r in records)
        )
        print("Patients:", len(patient_sets[split_name]))
        print("Saved:", output_path)

    print("\nSUCCESS: Patient-wise split completed.")
    print("No patient is shared between the splits.")


if __name__ == "__main__":
    main()
