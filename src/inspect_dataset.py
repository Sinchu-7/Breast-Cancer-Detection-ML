import numpy as np
from sklearn.datasets import load_breast_cancer

# Load the dataset
data = load_breast_cancer()

# Separate input features and target
X = data.data
y = data.target

# Display dataset dimensions
print("Dataset Inspection")
print("------------------")

print("X shape:", X.shape)
print("y shape:", y.shape)

# Count target classes
classes, counts = np.unique(y, return_counts=True)

print("\nClass Distribution:")

for class_id, count in zip(classes, counts):
    print(data.target_names[class_id], ":", count)

# Check missing values
print("\nMissing Values:", np.isnan(X).sum())

# Display feature information
print("\nTotal Features:", len(data.feature_names))