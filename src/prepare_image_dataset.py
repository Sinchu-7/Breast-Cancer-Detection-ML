
import os
import re
import glob
import json
from collections import defaultdict

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


def get_patient_id(filepath):
    filename = os.path.splitext(os.path.basename(filepath))[0]
    return re.sub(r"-(40|100|200|400)-\d+$", "", filename)


def collect_images():
    paths = []
    labels = []
    groups = []

    for label, class_name in enumerate(CLASSES):
        for magnification in MAGNIFICATIONS:
            folder = os.path.join(
                DATASET_DIR, magnification, class_name
            )

            files = glob.glob(os.path.join(folder, "*.png"))

            for filepath in files:
                paths.append(os.path.abspath(filepath))
                labels.append(label)
                groups.append(get_patient_id(filepath))

    return paths, labels, groups


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    paths, labels, groups = collect_images()

    print("Total images:", len(paths))
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
