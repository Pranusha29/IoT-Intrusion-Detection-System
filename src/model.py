import tensorflow as tf
from tensorflow import keras

Model = keras.Model

Input = keras.layers.Input
Conv1D = keras.layers.Conv1D
LSTM = keras.layers.LSTM
Dense = keras.layers.Dense
Dropout = keras.layers.Dropout
Layer = keras.layers.Layer


class Attention(Layer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self, input_shape):

        self.W = self.add_weight(
            name="attention_weight",
            shape=(input_shape[-1], 1),
            initializer="glorot_uniform",
            trainable=True
        )

        self.b = self.add_weight(
            name="attention_bias",
            shape=(input_shape[1], 1),
            initializer="zeros",
            trainable=True
        )

        super().build(input_shape)

    def call(self, inputs):

        scores = tf.nn.tanh(
            tf.matmul(inputs, self.W) + self.b
        )

        weights = tf.nn.softmax(
            scores,
            axis=1
        )

        context = tf.reduce_sum(
            inputs * weights,
            axis=1
        )

        return context


def build_model(
    timesteps=5,
    num_features=39,
    num_classes=34
):

    inputs = Input(
        shape=(timesteps, num_features)
    )

    # CNN layer
    x = Conv1D(
        filters=64,
        kernel_size=3,
        activation="relu",
        padding="same"
    )(inputs)

    # LSTM layer
    x = LSTM(
        64,
        return_sequences=True
    )(x)

    # Attention layer
    x = Attention()(x)

    # Classification layers
    x = Dense(
        64,
        activation="relu"
    )(x)

    x = Dropout(0.3)(x)

    outputs = Dense(
        num_classes,
        activation="softmax"
    )(x)

    model = Model(
        inputs=inputs,
        outputs=outputs
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=0.001
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model