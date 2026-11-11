
from dataclasses import dataclass
from numbers import Integral


@dataclass(frozen=True)
class DatasetSplitConfig:
    """Configuration for reproducible patient-wise dataset splitting."""

    n_splits: int = 5
    random_state: int = 42

    def __post_init__(self):
        if (
            isinstance(self.n_splits, bool)
            or not isinstance(self.n_splits, Integral)
        ):
            raise ValueError("n_splits must be an integer.")

        if self.n_splits < 2:
            raise ValueError("n_splits must be at least 2.")

        if (
            isinstance(self.random_state, bool)
            or not isinstance(self.random_state, Integral)
        ):
            raise ValueError("random_state must be an integer.")

        if self.random_state < 0:
            raise ValueError("random_state cannot be negative.")
