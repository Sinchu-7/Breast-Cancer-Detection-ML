
from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetSplitConfig:
    """Configuration for reproducible patient-wise dataset splitting."""

    n_splits: int = 5
    random_state: int = 42

    def __post_init__(self):
        if self.n_splits < 2:
            raise ValueError("n_splits must be at least 2.")

        if self.random_state < 0:
            raise ValueError("random_state cannot be negative.")
