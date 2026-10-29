import numpy as np
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


def evaluate_model(model, X_test, y_test, class_names=None):
    """
    Evaluate the trained model on test sequences.

    Returns:
        test_loss
        test_accuracy
        y_pred
        classification_report
        confusion_matrix
    """

    # Model evaluation
    test_loss, test_accuracy = model.evaluate(
        X_test,
        y_test,
        batch_size=512,
        verbose=1
    )

    # Predictions
    probabilities = model.predict(
        X_test,
        batch_size=512,
        verbose=1
    )

    y_pred = np.argmax(probabilities, axis=1)

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    # Classification report
    report = classification_report(
        y_test,
        y_pred,
        target_names=class_names,
        zero_division=0
    )

    # Confusion matrix
    cm = confusion_matrix(
        y_test,
        y_pred
    )

    print("\nTest Loss:", test_loss)
    print("Test Accuracy:", test_accuracy)
    print("Accuracy Score:", accuracy)

    print("\nClassification Report:")
    print(report)

    print("\nConfusion Matrix Shape:", cm.shape)

    return (
        test_loss,
        test_accuracy,
        y_pred,
        report,
        cm
    )