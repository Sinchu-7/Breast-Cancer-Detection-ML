
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer

# Step 1: Load dataset
data = load_breast_cancer()

X = data.data
y = data.target
feature_names = data.feature_names
target_names = data.target_names

print("DATA VISUALIZATION")
print("==================")

# Step 2: Class distribution
classes, counts = np.unique(y, return_counts=True)

plt.figure(figsize=(7, 5))
plt.bar(target_names, counts)

plt.title("Breast Cancer Class Distribution")
plt.xlabel("Cancer Class")
plt.ylabel("Number of Samples")

plt.tight_layout()
plt.show()

# Step 3: Mean radius comparison
radius_index = list(feature_names).index("mean radius")

malignant_radius = X[y == 0, radius_index]
benign_radius = X[y == 1, radius_index]

plt.figure(figsize=(7, 5))
plt.boxplot(
    [malignant_radius, benign_radius],
    tick_labels=["Malignant", "Benign"]
)

plt.title("Mean Radius Comparison")
plt.xlabel("Cancer Class")
plt.ylabel("Mean Radius")

plt.tight_layout()
plt.show()

# Step 4: Mean area comparison
area_index = list(feature_names).index("mean area")

malignant_area = X[y == 0, area_index]
benign_area = X[y == 1, area_index]

plt.figure(figsize=(7, 5))
plt.boxplot(
    [malignant_area, benign_area],
    tick_labels=["Malignant", "Benign"]
)

plt.title("Mean Area Comparison")
plt.xlabel("Cancer Class")
plt.ylabel("Mean Area")

plt.tight_layout()
plt.show()

# Step 5: Completion message
print("\nData Visualization Completed Successfully!")
