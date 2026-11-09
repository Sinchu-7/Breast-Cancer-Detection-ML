
import os
import joblib

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Step 1: Load the dataset
data = load_breast_cancer()

X = data.data
y = data.target

print("BREAST CANCER DETECTION")
print("=======================")

print("\nDataset Shape:", X.shape)

# Step 2: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", X_train.shape[0])
print("Testing Samples:", X_test.shape[0])

# Step 3: Create the machine learning pipeline
model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Step 4: Train the model
print("\nTraining Logistic Regression Model...")

model.fit(X_train, y_train)

print("Model Training Completed!")

# Step 5: Evaluate basic accuracy
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nMODEL PERFORMANCE")
print("-----------------")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Step 6: Save the trained model
os.makedirs("models", exist_ok=True)

model_path = os.path.join("models", "breast_cancer_model.pkl")

joblib.dump(model, model_path)

print("\nModel Saved Successfully!")
print("Saved Location:", model_path)

print("\nDay 9 Model Training Completed!")
