
import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)

# -------------------------------
# CONFIGURATION
# -------------------------------

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 15

TRAIN_JSON = "data/image_splits/train.json"
VAL_JSON = "data/image_splits/validation.json"

MODEL_DIR = "models"
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "breast_histopathology_mobilenetv2.keras"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# Label mapping:
# 0 = benign
# 1 = malignant


# -------------------------------
# LOAD SPLIT INFORMATION
# -------------------------------

def load_split(json_path):
    with open(json_path, "r", encoding="utf-8") as file:
        records = json.load(file)

    paths = [record["path"] for record in records]
    labels = [record["label"] for record in records]

    return paths, labels


train_paths, train_labels = load_split(TRAIN_JSON)
val_paths, val_labels = load_split(VAL_JSON)

print("Training images:", len(train_paths))
print("Validation images:", len(val_paths))


# -------------------------------
# IMAGE PREPROCESSING
# -------------------------------

def preprocess_image(path, label):
    image = tf.io.read_file(path)

    image = tf.io.decode_png(
        image,
        channels=3
    )

    image = tf.image.resize(
        image,
        IMAGE_SIZE
    )

    image = preprocess_input(image)

    label = tf.cast(label, tf.float32)

    return image, label


def create_dataset(paths, labels, training=False):
    dataset = tf.data.Dataset.from_tensor_slices(
        (paths, labels)
    )

    if training:
        dataset = dataset.shuffle(
            buffer_size=len(paths),
            seed=42
        )

    dataset = dataset.map(
        preprocess_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)

    return dataset


train_dataset = create_dataset(
    train_paths,
    train_labels,
    training=True
)

val_dataset = create_dataset(
    val_paths,
    val_labels
)


# -------------------------------
# HANDLE CLASS IMBALANCE
# -------------------------------

counts = np.bincount(
    train_labels,
    minlength=2
)

total = len(train_labels)

class_weights = {
    0: total / (2.0 * counts[0]),
    1: total / (2.0 * counts[1])
}

print("\nClass weights:", class_weights)


# -------------------------------
# BUILD MOBILENETV2 MODEL
# -------------------------------

base_model = MobileNetV2(
    weights="imagenet",
    include_top=False,
    input_shape=(224, 224, 3)
)

# Freeze pretrained layers initially
base_model.trainable = False

inputs = layers.Input(
    shape=(224, 224, 3)
)

features = base_model(
    inputs,
    training=False
)

features = layers.GlobalAveragePooling2D()(features)

features = layers.Dropout(0.3)(features)

outputs = layers.Dense(
    1,
    activation="sigmoid"
)(features)

model = models.Model(
    inputs=inputs,
    outputs=outputs
)


# -------------------------------
# COMPILE MODEL
# -------------------------------

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.AUC(name="auc")
    ]
)

model.summary()


# -------------------------------
# TRAINING CALLBACKS
# -------------------------------

callbacks = [
    ModelCheckpoint(
        MODEL_PATH,
        monitor="val_auc",
        mode="max",
        save_best_only=True,
        verbose=1
    ),

    EarlyStopping(
        monitor="val_auc",
        mode="max",
        patience=4,
        restore_best_weights=True,
        verbose=1
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=0.000001,
        verbose=1
    )
]


# -------------------------------
# TRAIN MODEL
# -------------------------------

print("\nStarting MobileNetV2 training...")

history = model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)


# -------------------------------
# SAVE FINAL MODEL
# -------------------------------

model.save(MODEL_PATH)

print("\nTraining completed!")
print("Model saved to:", MODEL_PATH)
print("Class mapping: 0 = benign, 1 = malignant")
