
import os
import json
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.callbacks import (
    ModelCheckpoint,
    EarlyStopping,
    ReduceLROnPlateau
)

MODEL_PATH = "models/breast_histopathology_mobilenetv2.keras"
FINETUNED_PATH = "models/breast_histopathology_mobilenetv2_finetuned.keras"

TRAIN_JSON = "data/image_splits/train.json"
VAL_JSON = "data/image_splits/validation.json"

IMAGE_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 10

# Load image split data
def load_split(path):
    with open(path, "r", encoding="utf-8") as file:
        records = json.load(file)

    paths = [r["path"] for r in records]
    labels = [r["label"] for r in records]

    return paths, labels


train_paths, train_labels = load_split(TRAIN_JSON)
val_paths, val_labels = load_split(VAL_JSON)


# Preprocessing
def preprocess_image(path, label):
    image = tf.io.read_file(path)
    image = tf.io.decode_png(image, channels=3)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = preprocess_input(image)

    return image, tf.cast(label, tf.float32)


def create_dataset(paths, labels, training=False):
    dataset = tf.data.Dataset.from_tensor_slices(
        (paths, labels)
    )

    if training:
        dataset = dataset.shuffle(
            len(paths),
            seed=42
        )

    dataset = dataset.map(
        preprocess_image,
        num_parallel_calls=tf.data.AUTOTUNE
    )

    return dataset.batch(BATCH_SIZE).prefetch(
        tf.data.AUTOTUNE
    )


train_dataset = create_dataset(
    train_paths, train_labels, training=True
)

val_dataset = create_dataset(
    val_paths, val_labels
)


# Class weights
counts = np.bincount(train_labels, minlength=2)
total = len(train_labels)

class_weights = {
    0: total / (2.0 * counts[0]),
    1: total / (2.0 * counts[1])
}


# Load previously trained model
print("Loading existing model...")

model = tf.keras.models.load_model(MODEL_PATH)

# Find MobileNetV2 inside the existing model
base_model = next(
    layer for layer in model.layers
    if isinstance(layer, tf.keras.Model)
)

print("Base model:", base_model.name)


# Unfreeze the final 30 layers
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

# Keep BatchNormalization layers frozen
for layer in base_model.layers:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

print("Trainable base model layers:",
      sum(layer.trainable for layer in base_model.layers))


# Recompile with a smaller learning rate
model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="binary_crossentropy",
    metrics=[
        "accuracy",
        tf.keras.metrics.Precision(name="precision"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.AUC(name="auc")
    ]
)


# Save the best fine-tuned model
callbacks = [
    ModelCheckpoint(
        FINETUNED_PATH,
        monitor="val_auc",
        mode="max",
        save_best_only=True,
        verbose=1
    ),

    EarlyStopping(
        monitor="val_auc",
        mode="max",
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),

    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=2,
        min_lr=0.0000001,
        verbose=1
    )
]


print("\nStarting fine-tuning...")

model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

print("\nFine-tuning completed!")
print("Best model saved to:", FINETUNED_PATH)
