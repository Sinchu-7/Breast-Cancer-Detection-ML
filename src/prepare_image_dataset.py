
import os
import re
import json
from pathlib import Path

from sklearn.model_selection import StratifiedGroupKFold

from src.dataset_config import DatasetSplitConfig


# ============================================================
# CONFIGURATION
# ============================================================

DATASET_DIR = (
    r"C:\Users\sinch\Downloads\BreakHis - Breast Cancer Histopathological Database"
    r"\BreakHis - Breast Cancer Histopathological Database"
    r"\images\dataset_cancer_v1\classificacao_binaria"
)

OUTPUT_DIR = "data/image_splits"

CLASSES = ["benign", "malignant"]
MAGNIFICATIONS = ["40X", "100X", "200X", "400X"]

SUPPORTED_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".tif", ".tiff"
}


# ============================================================
# FILENAME VALIDATION
# ============================================================

def validate_image_filename(filepath, expected_magnification=None):
    """Validate a BreakHis filename and optional folder magnification."""

    filename = Path(filepath).stem

    # Actual BreakHis naming convention.
    full_pattern = (
        r"^SOB_[BM]_[A-Z]-\d+-[A-Za-z0-9]+-"
        r"(40|100|200|400)-(\d+)$"
    )

    # Short naming convention used by existing unit tests.
    short_pattern = (
        r"^SOB_[BM]_[A-Z]-(40|100|200|400)-(\d+)$"
    )

    match = (
        re.fullmatch(full_pattern, filename)
        or re.fullmatch(short_pattern, filename)
    )

    if not match:
        raise ValueError(
            f"Invalid BreakHis filename format: {Path(filepath).name}"
        )

    magnification = f"{match.group(1)}X"

    if expected_magnification is not None:
        if magnification != expected_magnification:
            raise ValueError(
                f"Filename magnification {magnification} does not match "
                f"folder magnification {expected_magnification}: "
                f"{Path(filepath).name}"
            )

    return True


def get_patient_id(filepath):
    """Extract patient ID without requiring filename validation."""

    filename = Path(filepath).stem

    return re.sub(
        r"-(40|100|200|400)-\d+$",
        "",
        filename
    )


# ============================================================
# DATASET STRUCTURE VALIDATION
# ============================================================

def validate_dataset_structure(dataset_dir=DATASET_DIR):
    """Validate all expected class and magnification folders."""

    root = Path(dataset_dir)

    if not root.is_dir():
        raise FileNotFoundError(
            f"Dataset directory not found: {root}"
        )

    total_images = 0

    print("\n========== DATASET STRUCTURE VALIDATION ==========")

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:

            folder = root / magnification / class_name

            if not folder.is_dir():
                raise FileNotFoundError(
                    f"Dataset folder missing: {folder}"
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

            count = len(images)
            total_images += count

            print(
                f"{magnification} | {class_name}: {count} images"
            )

    print(f"\nTotal images: {total_images}")
    print("Dataset structure validation successful.")

    return total_images


# ============================================================
# IMAGE COLLECTION
# ============================================================

def collect_images(dataset_dir=DATASET_DIR):
    """Collect image paths, labels, and patient groups."""

    root = Path(dataset_dir)

    validate_dataset_structure(root)

    all_paths = []
    all_labels = []
    all_groups = []

    seen_paths = set()

    print("\n========== COLLECTING DATASET IMAGES ==========")

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:

            folder = root / magnification / class_name
            label = CLASSES.index(class_name)

            images = sorted(
                file for file in folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in SUPPORTED_EXTENSIONS
            )

            for image in images:

                validate_image_filename(
                    image,
                    expected_magnification=magnification
                )

                normalized_path = os.path.normcase(
                    os.path.abspath(str(image))
                )

                if normalized_path in seen_paths:
                    raise ValueError(
                        f"Duplicate image path found: {image}"
                    )

                seen_paths.add(normalized_path)

                patient_id = get_patient_id(image)

                all_paths.append(str(image))
                all_labels.append(label)
                all_groups.append(patient_id)

    if not all_paths:
        raise ValueError("No images found in dataset.")

    if not (
        len(all_paths) == len(all_labels) == len(all_groups)
    ):
        raise ValueError(
            "Image paths, labels, and groups have different lengths."
        )

    print(f"Collected images: {len(all_paths)}")
    print(f"Unique patients: {len(set(all_groups))}")

    return all_paths, all_labels, all_groups


# ============================================================
# SPLIT INTEGRITY VALIDATION
# ============================================================

def validate_splits(splits, all_paths, all_groups):
    """Validate split completeness and patient separation."""

    required_splits = {"train", "validation", "test"}

    if set(splits.keys()) != required_splits:
        raise ValueError(
            "Splits must contain exactly train, validation, and test."
        )

    if len(all_paths) != len(all_groups):
        raise ValueError(
            "Image paths and patient groups have different lengths."
        )

    all_path_set = {
        os.path.normcase(os.path.abspath(path))
        for path in all_paths
    }

    if len(all_path_set) != len(all_paths):
        raise ValueError(
            "Duplicate image paths found in the original dataset."
        )

    split_path_sets = {}
    patient_sets = {}

    path_to_patient = {
        os.path.normcase(os.path.abspath(path)): group
        for path, group in zip(all_paths, all_groups)
    }

    for split_name, paths in splits.items():

        if not paths:
            raise ValueError(
                f"{split_name} split is empty."
            )

        normalized_paths = [
            os.path.normcase(os.path.abspath(path))
            for path in paths
        ]

        if len(normalized_paths) != len(set(normalized_paths)):
            raise ValueError(
                f"Duplicate image found in {split_name} split."
            )

        split_path_sets[split_name] = set(normalized_paths)

        unknown_paths = (
            split_path_sets[split_name] - all_path_set
        )

        if unknown_paths:
            raise ValueError(
                f"Extra image paths found in {split_name} split."
            )

        patient_sets[split_name] = {
            path_to_patient[path]
            for path in split_path_sets[split_name]
        }

    # Check duplicate images across different splits first.
    split_names = ["train", "validation", "test"]

    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):

            first = split_names[i]
            second = split_names[j]

            overlap = (
                split_path_sets[first]
                & split_path_sets[second]
            )

            if overlap:
                raise ValueError(
                    f"Duplicate images between {first} and {second}."
                )

    combined_paths = set().union(
        *split_path_sets.values()
    )

    if combined_paths != all_path_set:
        raise ValueError(
            "Dataset splits contain missing or extra image paths."
        )

    # Check patient leakage.
    for i in range(len(split_names)):
        for j in range(i + 1, len(split_names)):

            first = split_names[i]
            second = split_names[j]

            overlap = patient_sets[first] & patient_sets[second]

            if overlap:
                raise ValueError(
                    f"Patient leakage between {first} and {second}: "
                    f"{sorted(overlap)}"
                )

    return patient_sets


# ============================================================
# DATASET SPLITTING
# ============================================================

def main(config=None):
    """Create patient-wise train, validation, and test splits."""

    if config is None:
        config = DatasetSplitConfig()

    all_paths, all_labels, all_groups = collect_images()

    print("\n========== CREATING DATASET SPLITS ==========")

    outer_splitter = StratifiedGroupKFold(
        n_splits=config.n_splits,
        shuffle=True,
        random_state=config.random_state
    )

    development_indices, test_indices = next(
        outer_splitter.split(
            all_paths,
            all_labels,
            all_groups
        )
    )

    development_paths = [
        all_paths[i] for i in development_indices
    ]

    development_labels = [
        all_labels[i] for i in development_indices
    ]

    development_groups = [
        all_groups[i] for i in development_indices
    ]

    test_paths = [
        all_paths[i] for i in test_indices
    ]

    inner_splitter = StratifiedGroupKFold(
        n_splits=config.n_splits,
        shuffle=True,
        random_state=config.random_state
    )

    train_indices, validation_indices = next(
        inner_splitter.split(
            development_paths,
            development_labels,
            development_groups
        )
    )

    train_paths = [
        development_paths[i] for i in train_indices
    ]

    validation_paths = [
        development_paths[i] for i in validation_indices
    ]

    splits = {
        "train": train_paths,
        "validation": validation_paths,
        "test": test_paths
    }

    patient_sets = validate_splits(
        splits,
        all_paths,
        all_groups
    )

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    for split_name, paths in splits.items():

        records = []

        for image_path in paths:

            image = Path(image_path)
            class_name = image.parent.name
            patient_id = get_patient_id(image)

            records.append({
                "path": str(image),
                "label": CLASSES.index(class_name),
                "class": class_name,
                "patient_id": patient_id
            })

        output_file = output_dir / f"{split_name}.json"

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)

        print(
            f"{split_name.capitalize()}: "
            f"{len(records)} images | "
            f"{len(patient_sets[split_name])} patients"
        )

    print("\nDataset splitting completed successfully.")
    print(f"Split files saved in: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
