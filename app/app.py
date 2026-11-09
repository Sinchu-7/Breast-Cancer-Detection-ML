
import streamlit as st
import tensorflow as tf
import numpy as np

from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


# -------------------------------
# CONFIGURATION
# -------------------------------

MODEL_PATH = (
    "models/breast_histopathology_mobilenetv2.keras"
)

IMAGE_SIZE = (224, 224)

CLASS_NAMES = ["Benign", "Malignant"]


# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Breast Cancer AI",
    page_icon="🎗️",
    layout="wide"
)


# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0B1120;
    color: #F1F5F9;
}

[data-testid="stSidebar"] {
    background-color: #151F32;
}

.main-title {
    font-size: 38px;
    font-weight: bold;
    color: #F47291;
}

.subtitle {
    color: #94A3B8;
    font-size: 17px;
}

.result-card {
    padding: 25px;
    border-radius: 15px;
    background-color: #151F32;
    border: 1px solid #263449;
}

.warning {
    padding: 15px;
    border-radius: 10px;
    background-color: #332719;
    color: #FBBF24;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# LOAD MODEL
# -------------------------------

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)


# -------------------------------
# PREDICTION FUNCTION
# -------------------------------

def predict_image(image, model):

    image = image.convert("RGB")
    resized_image = image.resize(IMAGE_SIZE)

    image_array = np.array(
        resized_image,
        dtype=np.float32
    )

    image_array = preprocess_input(image_array)

    image_array = np.expand_dims(
        image_array,
        axis=0
    )

    prediction = model.predict(
        image_array,
        verbose=0
    )[0][0]

    if prediction >= 0.5:
        predicted_class = "Malignant"
        confidence = prediction * 100
    else:
        predicted_class = "Benign"
        confidence = (1 - prediction) * 100

    return predicted_class, confidence


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("🎗️ Breast Cancer AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Image Prediction",
        "Model Dashboard",
        "About"
    ]
)


# -------------------------------
# HOME PAGE
# -------------------------------

if page == "Home":

    st.markdown(
        '<div class="main-title">🎗️ Breast Cancer AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Deep Learning Based Histopathology Image Classification'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Project Overview")

        st.write("""
        This educational project uses deep learning to classify
        breast histopathology images into two categories:

        - Benign
        - Malignant

        The model is built using MobileNetV2 transfer learning
        and trained on the BreakHis image dataset.
        """)

        st.info(
            "Upload a histopathology image from the Image Prediction page."
        )

    with col2:
        st.subheader("Model Information")

        st.metric("Architecture", "MobileNetV2")
        st.metric("Image Input", "224 × 224")
        st.metric("Dataset Images", "7,909")
        st.metric("Classes", "2")

    st.divider()

    st.markdown("""
    <div class="warning">
    ⚠️ Educational research prototype only. This application is
    not a medical diagnostic system and must not be used to
    make healthcare decisions.
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# IMAGE PREDICTION PAGE
# -------------------------------

elif page == "Image Prediction":

    st.title("🔬 Histopathology Image Prediction")

    st.write(
        "Upload a breast histopathology microscope image "
        "to demonstrate the model."
    )

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:

        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Uploaded Image")
            st.image(
                image,
                caption="Uploaded histopathology image",
                use_container_width=True
            )

        with col2:

            st.subheader("Prediction")

            if st.button(
                "Analyze Image",
                type="primary",
                use_container_width=True
            ):

                try:
                    with st.spinner("Analyzing image..."):

                        model = load_model()

                        predicted_class, confidence = predict_image(
                            image,
                            model
                        )

                    if predicted_class == "Benign":

                        st.success(
                            f"Model prediction: {predicted_class}"
                        )

                    else:

                        st.error(
                            f"Model prediction: {predicted_class}"
                        )

                    st.metric(
                        "Model Confidence",
                        f"{confidence:.2f}%"
                    )

                    st.caption(
                        "Confidence is the model's output score, "
                        "not a medical probability."
                    )

                    st.warning(
                        "This prediction is experimental and "
                        "must not be interpreted as a diagnosis."
                    )

                except Exception as error:

                    st.error(
                        f"Prediction failed: {error}"
                    )


# -------------------------------
# MODEL DASHBOARD
# -------------------------------

elif page == "Model Dashboard":

    st.title("📊 Model Dashboard")

    st.write(
        "Results from the original model's held-out test set."
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Accuracy", "69.54%")
    col2.metric("Precision", "85.62%")
    col3.metric("Recall", "67.39%")
    col4.metric("F1-score", "75.42%")

    st.subheader("Confusion Matrix")

    st.write("""
    | Actual Class | Predicted Benign | Predicted Malignant |
    |---|---:|---:|
    | Benign | 363 | 125 |
    | Malignant | 360 | 744 |
    """)

    st.warning(
        "The model has limited performance and is not suitable "
        "for medical diagnosis."
    )


# -------------------------------
# ABOUT PAGE
# -------------------------------

elif page == "About":

    st.title("ℹ️ About the Project")

    st.write("""
    ### Breast Cancer Histopathology Classification

    This project demonstrates an image classification workflow
    using deep learning.

    **Technologies used:**
    - Python
    - TensorFlow
    - Keras
    - MobileNetV2
    - Streamlit
    - Scikit-learn
    - BreakHis dataset

    **Classification categories:**
    - Benign
    - Malignant

    **Dataset:** BreakHis breast histopathology images.

    **Purpose:** Educational and research demonstration only.
    """)

    st.warning(
        "This application is not clinically validated. "
        "Consult qualified medical professionals for healthcare decisions."
    )
