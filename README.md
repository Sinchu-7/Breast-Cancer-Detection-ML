
# 🎗️ Breast Cancer Detection Using Deep Learning

### Histopathological Image Classification | Python | TensorFlow | MobileNetV2

An educational deep learning project that classifies breast histopathology images into **Benign** and **Malignant** categories using Transfer Learning with MobileNetV2.

> ⚠️ **Disclaimer:** This project is developed for educational and research purposes only. It is not a medical diagnostic tool and must not be used to make clinical decisions.

---

## 📌 Project Overview

Breast cancer is one of the most common cancers worldwide. This project explores how deep learning and computer vision can help classify histopathological breast tissue images.

The system uses a pretrained **MobileNetV2** model to extract image features and perform binary classification.

**Prediction classes:**
- Benign
- Malignant

## ✨ Features

- Histopathological image classification
- MobileNetV2 transfer learning
- Image upload and prediction
- Model evaluation using classification metrics
- Fine-tuning of pretrained layers
- Patient-wise dataset splitting
- Dataset statistics and distribution analysis
- Dataset filename and structure validation
- JSON split-file integrity validation
- Structured logging for dataset operations
- Automated unit testing
- Interactive Vite frontend and FastAPI prediction service
- Demo sign-in page for the research workspace
- Model performance dashboard

## 🧰 Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Deep Learning | TensorFlow, Keras |
| Model | MobileNetV2 |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Image Processing | Pillow |
| Visualization | Matplotlib, Seaborn |
| Web Application | Vite, FastAPI |
| Testing | Pytest |
| Logging | Python Logging |
| Version Control | Git, GitHub |

## 📂 Dataset

**Dataset:** BreakHis – Breast Cancer Histopathological Database

- Total images: 7,909
- Unique patients: 82
- Benign images: 2,480
- Malignant images: 5,429
- Image size: 224 × 224 pixels
- Magnification levels: 40X, 100X, 200X, 400X

The project uses the binary classification dataset.

The dataset is not included in this GitHub repository. Download and extract it separately before preparing the image splits.

### Class Distribution

| Class | Images | Percentage |
|---|---:|---:|
| Benign | 2,480 | 31.36% |
| Malignant | 5,429 | 68.64% |
| **Total** | **7,909** | **100%** |

### Magnification Distribution

| Magnification | Images | Percentage |
|---|---:|---:|
| 40X | 1,995 | 25.22% |
| 100X | 2,081 | 26.31% |
| 200X | 2,013 | 25.45% |
| 400X | 1,820 | 23.01% |

## ⚙️ Model Development

The project follows these steps:

1. Dataset preparation and image organization.
2. Patient-wise training, validation, and test splitting.
3. Image preprocessing and resizing.
4. MobileNetV2 transfer learning with pretrained ImageNet weights.
5. Model training with class weights.
6. Model evaluation using test data.
7. Fine-tuning selected pretrained layers.
8. Deployment using a Vite frontend and FastAPI prediction service.

Patient-wise splitting helps prevent images from the same patient appearing across different dataset splits.

## 📊 Dataset Split

| Split | Images | Patients |
|---|---:|---:|
| Training | 5,059 | 53 |
| Validation | 1,258 | 13 |
| Testing | 1,592 | 16 |
| **Total** | **7,909** | **82** |

## 🔍 Dataset Validation and Statistics

The project includes utilities for checking dataset quality and split integrity.

### Dataset Preparation

```bash
python -m src.prepare_image_dataset
```

Prepares patient-wise training, validation, and test splits.

### Dataset Statistics

```bash
python -m src.dataset_statistics
```

Generates:
- Total image count
- Unique patient count
- Benign and malignant distribution
- Magnification distribution
- Class and magnification percentages

### Split JSON Validation

```bash
python -m src.split_validation
```

Checks:
- Required JSON fields
- Valid class names and labels
- Duplicate image paths
- Patient leakage between splits
- Missing or invalid split files

### Automated Testing

Run the complete test suite:

```bash
python -m pytest -v
```

The tests cover dataset structure, patient ID extraction, split integrity, statistics, and JSON validation.

## 📈 Model Performance

The original MobileNetV2 model achieved the following results on the held-out test split:

| Metric | Score |
|---|---:|
| Accuracy | 69.54% |
| Precision | 85.62% |
| Recall | 67.39% |
| F1-score | 75.42% |

**Note:** These are experimental results from the current model. The test split was also used to compare the fine-tuned model, so it should not be treated as an untouched final test set for future model selection.

## 🗂️ Project Structure

```text
Breast-Cancer-Detection-ML/
├── backend/
│   ├── main.py
│   └── package.json
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.js
│       └── style.css
├── src/
│   ├── load_dataset.py
│   ├── inspect_dataset.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── dataset_config.py
│   ├── prepare_image_dataset.py
│   ├── dataset_statistics.py
│   ├── split_validation.py
│   ├── train_image_model.py
│   ├── evaluate_image_model.py
│   └── finetune_image_model.py
│
├── notebooks/
├── tests/
│   ├── test_backend_api.py
│   ├── test_image_dataset.py
│   ├── test_dataset_statistics.py
│   └── test_split_validation.py
│
├── docs/
├── data/
├── models/
├── reports/
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sinchu-7/Breast-Cancer-Detection-ML.git
```

### 2. Navigate to the project

```bash
cd Breast-Cancer-Detection-ML
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Prepare the image dataset

Download and extract the BreakHis dataset. Configure the dataset path in the preparation script if required.

```bash
python -m src.prepare_image_dataset
```

### 7. Train the image classification model

```bash
python -m src.train_image_model
```

### 8. Evaluate the model

```bash
python -m src.evaluate_image_model
```

### 9. Run the frontend and backend

In one terminal, install the frontend dependencies and start Vite:

```bash
cd frontend
npm install
npm run dev
```

In a second terminal, from the repository root, activate the Python environment created above and run:

```bash
cd backend
npm run dev
```

The frontend is served at `http://127.0.0.1:5173` and the API at `http://127.0.0.1:8000`. The trained model file must be available at `models/breast_histopathology_mobilenetv2.keras` for predictions; model weights are not included in this repository.

## 🖥️ Application Modules

- **Sign in:** Enter any valid email address and a non-empty password to open the demo workspace. This is a front-end-only flow: no credentials are sent to the backend or saved, and it does not provide account authentication.
- **Overview:** Dataset context and previously recorded model evaluation metrics.
- **Image analysis:** Upload a histopathology image and request a model classification.
- **Model & methods:** Review model details, validation metrics, and limitations.

## 🔮 Future Improvements

- Improve classification performance.
- Experiment with other CNN architectures.
- Improve malignant-class recall.
- Add more detailed visual explanations using Grad-CAM.
- Improve dashboard visualizations.
- Evaluate on an independent patient-level test dataset.

## 👩‍💻 Author

**Sinchana Poojary**

GitHub: [@Sinchu-7](https://github.com/Sinchu-7)

---
