import numpy as np


def create_sequences(X, y, sequence_length=5):
    """
    Create ordered traffic windows.

    Each window contains `sequence_length` consecutive records,
    and the target label is the label of the last record.
    """

    X_sequences = []
    y_sequences = []

    for i in range(len(X) - sequence_length + 1):
        X_sequences.append(
            X[i:i + sequence_length]
        )

        y_sequences.append(
            y[i + sequence_length - 1]
        )

    return np.array(X_sequences), np.array(y_sequences)