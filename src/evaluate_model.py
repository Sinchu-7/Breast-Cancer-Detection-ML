
import joblib
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

# Step 1: Load dataset
data = load_breast_cancer()

X = data.data
y = data.target
target_names = data.target_names

print("BREAST CANCER MODEL EVALUATION")
print("==============================")

# Step 2: Split dataset (same settings as training)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTesting Samples:", X_test.shape[0])

# Step 3: Load trained model
model = joblib.load("models/breast_cancer_model.pkl")

print("\nTrained Model Loaded Successfully!")

# Step 4: Make predictions
y_pred = model.predict(X_test)

# Step 5: Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(y_test, y_pred, zero_division=0)

recall = recall_score(y_test, y_pred, zero_division=0)

f1 = f1_score(y_test, y_pred, zero_division=0)

print("\nMODEL PERFORMANCE")
print("-----------------")

print("Accuracy :", round(accuracy * 100, 2), "%")
print("Precision:", round(precision * 100, 2), "%")
print("Recall   :", round(recall * 100, 2), "%")
print("F1 Score :", round(f1 * 100, 2), "%")

# Step 6: Classification report
print("\nCLASSIFICATION REPORT")
print("---------------------")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=target_names,
        zero_division=0
    )
)

# Step 7: Confusion matrix
cm = confusion_matrix(y_test, y_pred)

print("\nCONFUSION MATRIX")
print("----------------")
print(cm)

# Step 8: Display confusion matrix graph
display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=target_names
)

display.plot(cmap="Blues", values_format="d")

plt.title("Breast Cancer Model - Confusion Matrix")
plt.tight_layout()
plt.show()

print("\nDay 10 Model Evaluation Completed!")
