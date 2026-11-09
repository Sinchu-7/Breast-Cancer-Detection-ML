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
- Interactive Streamlit web application
- Model performance dashboard

## 🧠 Technologies Used

| Category | Technologies |
|---|---|
| Programming | Python |
| Deep Learning | TensorFlow, Keras |
| Model | MobileNetV2 |
| Data Processing | NumPy, Pandas |
| Machine Learning | Scikit-learn |
| Image Processing | Pillow |
| Visualization | Matplotlib, Seaborn |
| Web Application | Streamlit |
| Version Control | Git, GitHub |

## 📂 Dataset

**Dataset:** BreakHis – Breast Cancer Histopathological Database

- Total images: 7,909
- Benign images: 2,480
- Malignant images: 5,429
- Image size: 224 × 224 pixels
- Magnification levels: 40X, 100X, 200X, 400X

The project uses the binary classification dataset.

The dataset is not included in this GitHub repository. Download and extract it separately before preparing the image splits.

## ⚙️ Model Development

The project follows these steps:

1. Dataset preparation and image organization.
2. Patient-wise training, validation, and test splitting.
3. Image preprocessing and resizing.
4. MobileNetV2 transfer learning with pretrained ImageNet weights.
5. Model training with class weights.
6. Model evaluation using test data.
7. Fine-tuning selected pretrained layers.
8. Deployment using Streamlit.

Patient-wise splitting helps prevent images from the same patient appearing across different dataset splits.

## 📊 Dataset Split

| Split | Images | Patients |
|---|---:|---:|
| Training | 5,059 | 53 |
| Validation | 1,258 | 13 |
| Testing | 1,592 | 16 |
| **Total** | **7,909** | **82** |

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
│
├── app/
│   └── app.py
│
├── src/
│   ├── load_dataset.py
│   ├── inspect_dataset.py
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── evaluate_model.py
│   ├── predict.py
│   ├── prepare_image_dataset.py
│   ├── train_image_model.py
│   ├── evaluate_image_model.py
│   └── finetune_image_model.py
│
├── notebooks/
├── tests/
├── docs/
├── data/                 # Local dataset and split files
├── models/               # Locally trained models
├── reports/              # Evaluation reports
│
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
python src/prepare_image_dataset.py
```

### 7. Train the image classification model

```bash
python src/train_image_model.py
```

### 8. Evaluate the model

```bash
python src/evaluate_image_model.py
```

### 9. Run the Streamlit application

```bash
streamlit run app/app.py
```

Open the local URL displayed in your terminal to use the application.

## 🖥️ Application Modules

- **Home:** Project introduction and overview.
- **Image Prediction:** Upload a histopathology image for classification.
- **Model Dashboard:** View model evaluation metrics.
- **About:** Information about the project and technologies.

## 🔮 Future Improvements

- Improve classification performance.
- Experiment with other CNN architectures.
- Improve malignant-class recall.
- Add more detailed visual explanations using Grad-CAM.
- Improve dashboard visualizations.
- Evaluate on an independent patient-level test dataset.

## 👩‍💻 Author

**Sinchhh Poojary**

GitHub: [@Sinchu-7](https://github.com/Sinchu-7)

---

⭐ If you find this project interesting, consider giving the repository a star!