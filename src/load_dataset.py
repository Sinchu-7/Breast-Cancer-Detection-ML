from sklearn.datasets import load_breast_cancer

# Load the breast cancer dataset
data = load_breast_cancer()

# Display dataset information
print("Dataset loaded successfully!")

print("Number of samples:", data.data.shape[0])
print("Number of features:", data.data.shape[1])

print("Feature names:")
print(data.feature_names)

print("Target classes:")
print(data.target_names)

print("First 5 records:")
print(data.data[:5])