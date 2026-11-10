
import logging
from pathlib import Path
from collections import Counter

from src.prepare_image_dataset import (
    CLASSES,
    MAGNIFICATIONS,
    SUPPORTED_EXTENSIONS,
    get_patient_id,
)


# ============================================================
# LOGGING CONFIGURATION
# ============================================================

logger = logging.getLogger(__name__)


def generate_dataset_statistics(dataset_dir):
    """Generate image and patient statistics for the BreakHis dataset."""

    root = Path(dataset_dir)

    logger.info("Starting dataset statistics analysis.")

    if not root.is_dir():
        logger.error("Dataset directory not found: %s", root)
        raise FileNotFoundError(
            f"Dataset directory not found: {root}"
        )

    class_counts = Counter()
    magnification_counts = Counter()
    patient_ids = set()

    total_images = 0

    for magnification in MAGNIFICATIONS:
        for class_name in CLASSES:

            folder = root / magnification / class_name

            if not folder.is_dir():
                logger.error("Dataset folder missing: %s", folder)
                raise FileNotFoundError(
                    f"Dataset folder missing: {folder}"
                )

            try:
                images = sorted(
                    file for file in folder.iterdir()
                    if file.is_file()
                    and file.suffix.lower() in SUPPORTED_EXTENSIONS
                )

            except OSError:
                logger.exception(
                    "Unable to read dataset folder: %s", folder
                )
                raise

            if not images:
                logger.error(
                    "No supported images found in: %s", folder
                )
                raise ValueError(
                    f"No supported images found in: {folder}"
                )

            count = len(images)

            class_counts[class_name] += count
            magnification_counts[magnification] += count
            total_images += count

            for image in images:
                patient_ids.add(get_patient_id(image))

            logger.info(
                "Processed %s/%s: %d images",
                magnification,
                class_name,
                count,
            )

    if total_images == 0:
        logger.error("Dataset contains no images.")
        raise ValueError("Dataset contains no images.")

    statistics = {
        "total_images": total_images,
        "total_patients": len(patient_ids),
        "class_distribution": dict(class_counts),
        "magnification_distribution": dict(magnification_counts),
        "class_percentages": {
            class_name: round(
                count / total_images * 100, 2
            )
            for class_name, count in class_counts.items()
        },
        "magnification_percentages": {
            magnification: round(
                count / total_images * 100, 2
            )
            for magnification, count in magnification_counts.items()
        },
    }

    logger.info(
        "Dataset analysis completed: %d images, %d patients.",
        total_images,
        len(patient_ids),
    )

    return statistics


def print_dataset_statistics(statistics):
    """Display dataset statistics in a readable format."""

    print("\n========== BREAKHIS DATASET STATISTICS ==========")

    print("\nTotal images:", statistics["total_images"])
    print("Unique patients:", statistics["total_patients"])

    print("\nClass Distribution")

    for class_name, count in statistics["class_distribution"].items():
        percentage = statistics["class_percentages"][class_name]

        print(
            f"{class_name.capitalize()}: "
            f"{count} images ({percentage}%)"
        )

    print("\nMagnification Distribution")

    for magnification, count in statistics[
        "magnification_distribution"
    ].items():
        percentage = statistics["magnification_percentages"][
            magnification
        ]

        print(
            f"{magnification}: {count} images ({percentage}%)"
        )

    print("\n=================================================")


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    from src.prepare_image_dataset import DATASET_DIR

    try:
        dataset_stats = generate_dataset_statistics(DATASET_DIR)
        print_dataset_statistics(dataset_stats)

    except (FileNotFoundError, ValueError, OSError):
        logger.exception("Dataset statistics generation failed.")
        raise
