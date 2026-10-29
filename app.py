from flask_cors import CORS
from pathlib import Path
import csv
import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, jsonify, request
from tensorflow.keras.models import load_model

from src.model import Attention
# --------------------------------------------------
# Flask App
# --------------------------------------------------
app = Flask(__name__)
CORS(app)
# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "models" / "cnn_lstm_attention_final.keras"
SCALER_PATH = BASE_DIR / "models" / "ordered_scaler.pkl"
LABEL_MAPPING_PATH = (
    BASE_DIR / "results" / "metrics" / "label_mapping.csv"
)


# --------------------------------------------------
# Load trained model and preprocessing artifacts
# --------------------------------------------------

model = load_model(
    MODEL_PATH,
    custom_objects={"Attention": Attention}
)

scaler = joblib.load(SCALER_PATH)
print("Loaded model input shape:", model.input_shape)

label_mapping = pd.read_csv(
    LABEL_MAPPING_PATH
)# Load 8-category XGBoost model
BROAD_MODEL_PATH = BASE_DIR / "models" / "xgboost_iot_ids_final.pkl"
BROAD_ENCODER_PATH = BASE_DIR / "models" / "xgboost_iot_ids_final_encoder.pkl"

broad_model = joblib.load(BROAD_MODEL_PATH)
broad_encoder = joblib.load(BROAD_ENCODER_PATH)

print("Loaded 8-category XGBoost model successfully.")
print("Broad categories:", list(broad_encoder.classes_))

# --------------------------------------------------
# Feature configuration
# --------------------------------------------------

NUM_FEATURES = 39
SEQUENCE_LENGTH = 5


# --------------------------------------------------
# Home route
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({
    "message": "IoT Intrusion Detection API is running",
    "model": "Weighted XGBoost",
    "num_features": NUM_FEATURES,
    "num_classes": len(broad_encoder.classes_),
    "prediction_endpoint": "/predict_broad"
})


# --------------------------------------------------
# Prediction route
# --------------------------------------------------

@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = request.get_json()

        if data is None:
            return jsonify({
                "error": "Request body must contain JSON data."
            }), 400

        records = data.get("records")

        if records is None:
            return jsonify({
                "error": "Missing 'records' field."
            }), 400

        # Convert input to NumPy array
        X = np.array(records, dtype=float)

        # Validate shape
        if X.shape != (SEQUENCE_LENGTH, NUM_FEATURES):
            return jsonify({
                "error": (
                    f"Expected input shape "
                    f"({SEQUENCE_LENGTH}, {NUM_FEATURES}), "
                    f"but received {X.shape}."
                )
            }), 400

        # Scale using the same scaler used during training
        X_scaled = scaler.transform(X)

        # Add batch dimension
        X_sequence = X_scaled.reshape(
            1,
            SEQUENCE_LENGTH,
            NUM_FEATURES
        )

        # Model prediction
        probabilities = model.predict(
            X_sequence,
            verbose=0
        )[0]

        predicted_class = int(
            np.argmax(probabilities)
        )

        confidence = float(
            probabilities[predicted_class]
        )

        # Convert class ID to attack name
        predicted_name = label_mapping.loc[
            label_mapping["encoded_id"] == predicted_class,
            "label"
        ].iloc[0]

        return jsonify({
            "predicted_class_id": predicted_class,
            "predicted_attack": predicted_name,
            "confidence": confidence
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/predict_broad", methods=["POST"])
def predict_broad():
    try:
        data = request.get_json()

        if data is None or "records" not in data:
            return jsonify({
                "error": "Request JSON must contain a 'records' field."
            }), 400

        records = np.asarray(data["records"], dtype=float)

        if records.shape != (NUM_FEATURES,):
            return jsonify({
                "error": f"Expected exactly {NUM_FEATURES} features, received shape {records.shape}."
            }), 400

        if not np.isfinite(records).all():
            return jsonify({
                "error": "All feature values must be finite numbers."
            }), 400

        probabilities = broad_model.predict_proba(
            records.reshape(1, -1)
        )[0]

        predicted_id = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_id])

        predicted_category = str(
            broad_encoder.inverse_transform([predicted_id])[0]
        )

        return jsonify({
            "predicted_category": predicted_category,
            "confidence": confidence
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/shap", methods=["GET"])
def get_shap_results():
    shap_file = "results/metrics/shap_feature_importance.csv"

    if not os.path.exists(shap_file):
        return jsonify({
            "error": "SHAP results file not found."
        }), 404

    try:
        with open(shap_file, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        return jsonify({
            "features": rows[:10]
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# --------------------------------------------------
# Run application
# --------------------------------------------------

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
  