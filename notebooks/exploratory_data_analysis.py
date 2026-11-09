
import numpy as np
from sklearn.datasets import load_breast_cancer

# Step 1: Load dataset
data = load_breast_cancer()

X = data.data
y = data.target
feature_names = data.feature_names
target_names = data.target_names

print("EXPLORATORY DATA ANALYSIS")
print("=========================")

# Step 2: Dataset information
print("\nDataset Shape:", X.shape)
print("Total Samples:", len(X))
print("Total Features:", len(feature_names))

# Step 3: Class distribution
print("\nCLASS DISTRIBUTION")

classes, counts = np.unique(y, return_counts=True)

for class_id, count in zip(classes, counts):
    percentage = (count / len(y)) * 100
    print(
        target_names[class_id],
        ":",
        count,
        f"({percentage:.2f}%)"
    )

# Step 4: Calculate feature averages
print("\nAVERAGE FEATURE VALUES")

for i, feature in enumerate(feature_names):
    print(feature, ":", round(np.mean(X[:, i]), 4))

# Step 5: Compare selected features by class
print("\nCLASS-WISE FEATURE COMPARISON")

selected_features = ["mean radius", "mean texture", "mean area"]

for feature in selected_features:
    index = list(feature_names).index(feature)

    malignant_mean = np.mean(X[y == 0, index])
    benign_mean = np.mean(X[y == 1, index])

    print("\nFeature:", feature)
    print("Malignant Average:", round(malignant_mean, 4))
    print("Benign Average:", round(benign_mean, 4))
