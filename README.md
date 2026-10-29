# IoT Intrusion Detection System
# IoT Intrusion Detection System (IoT-IDS)

## Project Overview

This project implements an IoT Intrusion Detection System using the CICIoT2023 network traffic dataset. It explores deep learning and machine learning approaches for classifying IoT network traffic and identifying potential attacks.

The project includes two main experiments:

- **CNN-LSTM-Attention:** A deep learning baseline for 34-class fine-grained attack classification, achieving 77.34% test accuracy.
- **Weighted XGBoost:** The selected model for 8-category attack classification, achieving 82.93% test accuracy and a macro F1-score of 69.43%.

The final Flask API uses the weighted XGBoost model to predict one of eight broad traffic categories.

### Final Model Pipeline

CICIoT2023 Traffic → Preprocessing → 39 Features → Weighted XGBoost → 8-Category Prediction → Flask REST API

SHAP-based local explainability was explored separately with the CNN-LSTM-Attention experiment.

## Final Model Results

| Metric | Weighted XGBoost |
|---|---:|
| Test Accuracy | 82.93% |
| Macro F1-score | 69.43% |
| Weighted F1-score | 83.82% |
| Macro Precision | 76.51% |
| DoS Recall | 71.27% |

The original 8-category XGBoost model achieved 85.84% test accuracy. The weighted model achieved a higher macro F1-score and DoS recall, with a trade-off in overall accuracy.

The 8-category results should not be directly compared with the 34-class CNN-LSTM-Attention results as if they were the same classification task.

## Key Features

- **IoT Traffic Classification:** Classifies network traffic into eight broad categories using the selected weighted XGBoost model.
- **Deep Learning Experiment:** Includes a CNN-LSTM-Attention model for 34-class fine-grained attack classification.
- **Data Preprocessing:** Handles missing values, infinite values, and feature preparation for model prediction.
- **39 Network Features:** Uses 39 numerical traffic features from the CICIoT2023 dataset.
- **Attack Detection:** Identifies categories such as DDoS, DoS, Mirai, Recon, Spoofing, Brute Force, Web-based, and BENIGN.
- **Class Imbalance Handling:** Uses sample weighting in the final XGBoost model to improve minority-class performance.
- **SHAP Explainability:** Explores local prediction explanations for the CNN-LSTM-Attention experiment.
- **Flask REST API:** Provides the `/predict_broad` endpoint for eight-category predictions.

## Dataset

The project uses the **CICIoT2023 dataset** for IoT network intrusion detection.

### Dataset Details

- Dataset: CICIoT2023
- Features used: 39
- Target column: `Label`
- Number of attack classes: 34
- Data format: CSV
- Training/Test split: 80% / 20%
- Sequence length: 5 records

### Preprocessing

The following preprocessing operations are applied:

1. Separate the `Label` column from the network traffic features.
2. Replace infinite values with missing values.
3. Fill missing feature values using the feature-wise median.
4. Encode attack labels using `LabelEncoder`.
5. Preserve the original record order during the train/test split.
6. Fit `StandardScaler` only on the training data.
7. Transform both training and testing data using the fitted scaler.

## Model Architecture

The proposed deep learning model combines three main components:

### 1. CNN

A 1D Convolutional Neural Network is used to learn local patterns from the ordered traffic windows.

### 2. LSTM

The LSTM layer processes the sequence representation and learns dependencies between consecutive traffic records.

### 3. Attention Mechanism

The Attention layer assigns different weights to the LSTM outputs and helps the model focus on more relevant parts of the traffic sequence.

### Final Architecture

Input `(2, 39)`
↓
Conv1D – 64 filters, kernel size 2, ReLU activation
↓
LSTM – 64 units, return sequences enabled
↓
Attention Mechanism
↓
Dense – 64 units, ReLU activation
↓
Dropout – 0.3
↓
Dense – 34 classes, Softmax activation

### Model Parameters

- Input shape: `(2, 39)`
- Input features: 39
- Sequence length: 2 traffic records
- CNN filters: 64
- CNN kernel size: 2
- LSTM units: 64
- Attention mechanism: Trainable attention layer
- Dense units: 64
- Dropout: 0.3
- Output classes: 34
- Total trainable parameters: 44,516
- Optimizer: Adam
- Learning rate: 0.001
- Loss function: Sparse Categorical Crossentropy

## Training and Evaluation

The model is trained using the prepared ordered traffic windows.

### Training Configuration

- Training epochs: 3
- Batch size: 512
- Optimizer: Adam
- Learning rate: 0.001
- Loss function: Sparse Categorical Crossentropy
- Sequence length: 2 traffic records
- Number of input features: 39
- Number of output classes: 34
- Data split: 80% training and 20% testing
- Random seed: 42

### Evaluation Metrics

The trained model is evaluated using:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion Matrix

### Final Test Result

The reproducible CNN-LSTM-Attention baseline model using sequence length 2 achieved the following results on the 34-class CICIoT2023 classification task:

- **Test Accuracy:** 77.34%
- **Test Loss:** 0.4432
- **Macro F1-score:** 0.5392
- **Weighted F1-score:** 0.7533
- **Best Validation Accuracy:** 77.15%

The difference between macro F1-score and weighted F1-score reflects uneven performance across attack classes, particularly for underrepresented classes.

**Note:** These results correspond to the reproducible 2-record baseline model, not the earlier 5-record model.

### Weighted XGBoost — 8-Class Final Test Results

The weighted XGBoost model was evaluated on the held-out test dataset for the 8-category IoT intrusion detection task.

- **Test Accuracy:** 82.93%
- **Macro F1-score:** 69.43%
- **Weighted F1-score:** 83.83%
- **Macro Precision:** 76.51%

The weighted model improves the balance of detection across attack categories compared with the original unweighted model. However, Brute Force and Web-based attacks remain challenging minority classes.

**Test Confusion Matrix:** `results/figures/xgboost_weighted_8class_test_confusion_matrix.png`

**Metrics CSV:** `results/metrics/xgboost_weighted_8class_test_metrics.csv`

*Note: These results correspond to the 8-class XGBoost model used by the Flask API. They are separate from the 34-class CNN-LSTM-Attention baseline results reported above.*

## Explainability

To improve the interpretability of the deep learning model, **SHAP (SHapley Additive exPlanations)** is used.

The SHAP analysis explains which network traffic features contributed most to the model's prediction.

### SHAP Method

Due to compatibility issues with TensorFlow/Keras-specific SHAP explainers, the project uses **SHAP KernelExplainer**, a model-agnostic explanation method.

For the selected experiment, the traffic input was flattened into a feature vector before SHAP analysis and reshaped as required for model prediction.

The SHAP analysis used a background sample of 50 records and 100 samples for the KernelExplainer estimation.

### Example Explanation

For one selected test sample, the model predicted:

- **Predicted attack:** `DDOS-RSTFINFLOOD`
- **Confidence:** Approximately 99.9%

The top contributing features in this individual explanation were:

1. `fin_flag_number`
2. `fin_count`
3. `psh_flag_number`
4. `HTTPS`
5. `Tot sum`
6. `IPv`
7. `syn_count`
8. `rst_count`
9. `syn_flag_number`
10. `rst_flag_number`

These SHAP values represent contributions for one selected prediction. They should not be interpreted as global feature importance or percentages of model influence.

The SHAP feature contribution graph is saved at:

`results/figures/shap_top10_feature_contributions.png`

## Project Structure

```text
IoT-IDS/
├── data/
│   └── CICIoT2023/
│       ├── raw/
│       └── processed/
├── notebooks/
│   ├── 01_dataset_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_sequence_creation.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_shap_explainability.ipynb
├── src/
│   ├── preprocessing.py
│   ├── sequence.py
│   ├── model.py
│   ├── train.py
│   ├── evaluate.py
│   └── explainability.py
├── models/
│   ├── xgboost_iot_ids_final.pkl
│   └── xgboost_iot_ids_final_encoder.pkl
├── results/
│   ├── figures/
│   ├── metrics/
│   └── explanations/
├── app.py
├── requirements.txt
└── README.md

## Flask REST API

The project provides a Flask REST API that uses the trained weighted XGBoost model to classify IoT network traffic into eight broad categories.

### Endpoint

`POST /predict_broad`

### Request Format

Send a JSON object containing `records`, a list of 39 numerical network traffic features.

```json
{
  "records": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
```

Replace the example values with actual preprocessed network traffic features.

### Response Format

```json
{
  "confidence": 0.95,
  "predicted_category": "Spoofing"
}
```

The response illustrates the expected structure; the confidence and predicted category will depend on the input.

### Supported Categories

- BENIGN
- Brute Force
- DDoS
- DoS
- Mirai
- Recon
- Spoofing
- Web-based

## How to Run

### 1. Create and Activate Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Jupyter Notebooks

Open Jupyter Notebook or VS Code and execute the notebooks in the following order:

1. `01_dataset_exploration.ipynb`
2. `02_preprocessing.ipynb`
3. `03_sequence_creation.ipynb`
4. `04_model_training.ipynb`
5. `05_shap_explainability.ipynb`

### 4. Run the Flask API

```bash
python app.py
```

The API provides the `POST /predict_broad` endpoint for eight-category attack prediction using the weighted XGBoost model. Ensure the trained model and encoder files are available in the `models/` directory before running the application.

## Results

### CNN-LSTM-Attention — 34-Class Classification

The CNN-LSTM-Attention model was evaluated for fine-grained classification of 34 traffic labels.

| Metric | Result |
|---|---:|
| Test Accuracy | 77.34% |
| Test Loss | 0.4432 |
| Macro F1-score | 53.92% |
| Weighted F1-score | 75.33% |
| Best Validation Accuracy | 77.15% |

SHAP KernelExplainer was used to explore feature contributions for an individual CNN-LSTM-Attention prediction.

### Weighted XGBoost — 8-Category Classification

The weighted XGBoost model is the selected model used by the Flask API.

| Metric | Result |
|---|---:|
| Test Accuracy | 82.93% |
| Macro Precision | 76.51% |
| Macro F1-score | 69.43% |
| Weighted F1-score | 83.83% |
| DoS Recall | 71.27% |

The original, unweighted XGBoost model achieved 85.84% test accuracy and a macro F1-score of 67.24%. The weighted model improved macro F1-score and DoS recall, with a trade-off in overall accuracy.

**Note:** The CNN-LSTM-Attention and XGBoost results represent different classification tasks (34 classes versus 8 categories), so their metrics should not be treated as a direct, like-for-like comparison.

### Limitations

- The CICIoT2023 CSV files do not provide an obvious timestamp column for the selected data.
- Therefore, the model uses ordered traffic windows rather than claiming true temporal sequences.
- The overlapping windows can introduce dependency between samples.
- The dataset contains significant class imbalance, especially for rare attack classes.
- SHAP explanations are currently demonstrated as local explanations for selected samples.
- The current Flask API accepts 39 numerical features per prediction through the `/predict_broad` endpoint.

