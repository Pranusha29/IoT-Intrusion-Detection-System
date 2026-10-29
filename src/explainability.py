import numpy as np
import pandas as pd
import shap


def create_prediction_wrapper(model, timesteps=5, num_features=39):
    """
    Convert flattened SHAP input back to sequence format
    before passing it to the model.
    """

    def model_predict(X_flat):
        X_sequence = X_flat.reshape(
            -1,
            timesteps,
            num_features
        )

        return model.predict(
            X_sequence,
            verbose=0
        )

    return model_predict


def compute_kernel_shap(
    model,
    background_data,
    test_sample,
    timesteps=5,
    num_features=39,
    nsamples=100
):
    """
    Compute Kernel SHAP values for a single test sequence.

    Parameters:
        model          : trained CNN-LSTM-Attention model
        background_data: background sequences
        test_sample    : sequence to explain
        timesteps      : sequence length
        num_features   : number of features
        nsamples       : number of SHAP samples

    Returns:
        explainer
        shap_values
        predicted_class
        prediction
    """

    # Flatten sequence data for Kernel SHAP
    background_flat = background_data.reshape(
        background_data.shape[0],
        -1
    )

    test_flat = test_sample.reshape(
        test_sample.shape[0],
        -1
    )

    # Prediction wrapper
    model_predict = create_prediction_wrapper(
        model,
        timesteps,
        num_features
    )

    # Create Kernel SHAP explainer
    explainer = shap.KernelExplainer(
        model_predict,
        background_flat
    )

    # Calculate SHAP values
    shap_values = explainer.shap_values(
        test_flat,
        nsamples=nsamples,
        ranked_outputs=1
    )

    # Model prediction
    prediction = model.predict(
        test_sample,
        verbose=0
    )

    predicted_class = np.argmax(
        prediction[0]
    )

    return (
        explainer,
        shap_values,
        predicted_class,
        prediction
    )


def extract_feature_importance(
    shap_values,
    predicted_class,
    feature_names,
    timesteps=5,
    num_features=39
):
    """
    Convert SHAP values into feature-level importance.

    SHAP values from all timesteps are averaged using
    mean absolute SHAP value.
    """

    shap_array = shap_values[0]

    # Select SHAP values for predicted class
    shap_array = shap_array[:, predicted_class]

    # Convert 195 flattened features → 5 × 39
    shap_array = shap_array.reshape(
        timesteps,
        num_features
    )

    # Mean absolute contribution across timesteps
    feature_shap = np.mean(
        np.abs(shap_array),
        axis=0
    )

    shap_df = pd.DataFrame({
        "Feature": feature_names,
        "SHAP_Value": feature_shap
    })

    shap_df = shap_df.sort_values(
        "SHAP_Value",
        ascending=False
    ).reset_index(drop=True)

    return shap_df