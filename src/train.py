import sys
from pathlib import Path

import numpy as np
from sklearn.utils.class_weight import compute_class_weight

# Allow imports from src
sys.path.append(str(Path(__file__).resolve().parent))

from model import build_model


def train_model(
    X_train,
    y_train,
    X_val=None,
    y_val=None,
    epochs=15,
    batch_size=512
):
    """
    Train the CNN-LSTM-Attention model.

    Class weights are used to reduce the effect of class imbalance.
    """

    num_classes = len(np.unique(y_train))

    model = build_model(
        timesteps=X_train.shape[1],
        num_features=X_train.shape[2],
        num_classes=num_classes
    )

    # Calculate balanced class weights
    classes = np.unique(y_train)

    weights = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_train
    )

    class_weight_dict = dict(
        zip(classes, weights)
    )

    # Validation data
    validation_data = None

    if X_val is not None and y_val is not None:
        validation_data = (X_val, y_val)

    # Train
    history = model.fit(
        X_train,
        y_train,
        validation_data=validation_data,
        epochs=epochs,
        batch_size=batch_size,
        class_weight=class_weight_dict,
        shuffle=False,
        verbose=1
    )

    return model, history, class_weight_dict