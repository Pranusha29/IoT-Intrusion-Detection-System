import { useState } from "react";

function TrafficAnalysis() {
  const [records, setRecords] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [shapResults, setShapResults] = useState([]);

  const analyzeTraffic = async () => {
    setError("");
    setResult(null);
    setShapResults([]);

    try {
      const parsedData = JSON.parse(records);
      const parsedRecords = parsedData.records ?? parsedData;

      console.log("NUMBER OF RECORDS:", parsedRecords.length);
      console.log(
        "RECORD LENGTHS:",
        parsedRecords.map((record) => record.length)
      );

      if (!Array.isArray(parsedRecords) || parsedRecords.length !== 5) {
        throw new Error("Input must contain exactly 5 traffic records.");
      }

      parsedRecords.forEach((record) => {
        if (!Array.isArray(record) || record.length !== 39) {
          throw new Error(
            "Each traffic record must contain exactly 39 features."
          );
        }
      });

      setLoading(true);

      // Prediction API
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          records: parsedRecords,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Prediction failed.");
      }

      setResult(data);

      // SHAP API
      const shapResponse = await fetch("http://127.0.0.1:5000/shap");

      const shapData = await shapResponse.json();

      if (shapResponse.ok) {
        setShapResults(shapData.features);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section id="attack-detection" className="traffic-analysis">

      {/* Header */}
      <div className="analysis-header">
        <div>
          <p className="eyebrow">TRAFFIC ANALYSIS</p>

          <h2>Analyze Network Traffic</h2>

          <p>
            Submit a traffic window containing 5 records and 39 network
            traffic features for attack classification.
          </p>
        </div>

        <div className="analysis-model">
          CNN + LSTM + Attention
        </div>
      </div>

      {/* Input */}
      <div id="traffic-input" className="input-card">

        <label htmlFor="traffic-data">
          Traffic Window <span>5 × 39</span>
        </label>

        <textarea
          id="traffic-data"
          value={records}
          onChange={(e) => setRecords(e.target.value)}
          placeholder={`Paste your 5 × 39 traffic records as JSON...

Example:
[
  [feature1, feature2, ..., feature39],
  [feature1, feature2, ..., feature39],
  [feature1, feature2, ..., feature39],
  [feature1, feature2, ..., feature39],
  [feature1, feature2, ..., feature39]
]`}
        />

        <div className="input-info">
          <span>Required: 5 records</span>
          <span>39 features per record</span>
        </div>

        <button
          className="primary-btn analyze-button"
          onClick={analyzeTraffic}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Traffic →"}
        </button>
      </div>

      {/* Error */}
      {error && (
        <div className="error-card">
          <strong>Prediction Error</strong>
          <p>{error}</p>
        </div>
      )}

      {/* Prediction Result */}
      {result && (
        <div id="attack-detection" className="prediction-card">

          <div className="prediction-header">
            <div>
              <p className="eyebrow">DETECTION RESULT</p>
              <h3>Attack Detected</h3>
            </div>

            <span className="prediction-id">
              Class #{result.predicted_class_id}
            </span>
          </div>

          <div className="prediction-main">

            <div>
              <span className="result-label">
                PREDICTED ATTACK
              </span>

              <h2>{result.predicted_attack}</h2>
            </div>

            <div className="confidence">

              <span className="result-label">
                CONFIDENCE
              </span>

              <strong>
                {(result.confidence * 100).toFixed(2)}%
              </strong>

            </div>

          </div>

          <div className="confidence-bar">
            <div
              style={{
                width: `${result.confidence * 100}%`,
              }}
            ></div>
          </div>

        </div>
      )}

      {/* SHAP Results */}
      {shapResults.length > 0 && (
        <div className="shap-results-card">

          <div className="prediction-header">

            <div>
              <p className="eyebrow">MODEL INSIGHTS</p>

              <h3>SHAP Feature Importance</h3>
            </div>

            <span className="ready-badge">
              SHAP
            </span>

          </div>

          <p className="shap-description">
            These features had the strongest influence on the model's
            prediction.
          </p>

          <div className="shap-list">

            {shapResults.map((item, index) => {

              const shapValue = Number(item.SHAP_Value);

              const firstValue = Math.abs(
                Number(shapResults[0].SHAP_Value)
              );

              const barWidth =
                firstValue > 0
                  ? Math.min(
                      (Math.abs(shapValue) / firstValue) * 100,
                      100
                    )
                  : 0;

              return (
                <div className="shap-row" key={index}>

                  <span className="shap-rank">
                    #{index + 1}
                  </span>

                  <span className="shap-feature">
                    {item.Feature}
                  </span>

                  <span className="shap-value">
                    {shapValue.toFixed(5)}
                  </span>

                  <div className="shap-bar-container">

                    <div
                      className="shap-bar"
                      style={{
                        width: `${barWidth}%`,
                      }}
                    ></div>

                  </div>

                </div>
              );
            })}

          </div>
        </div>
      )}

      {/* Prediction Summary */}
      {result && (
        <div className="prediction-summary-card">

          <div className="prediction-header">

            <div>
              <p className="eyebrow">
                PREDICTION SUMMARY
              </p>

              <h3>Analysis Overview</h3>
            </div>

            <span className="ready-badge">
              COMPLETED
            </span>

          </div>

          <div className="summary-grid">

            <div className="summary-item">
              <span>DETECTED ATTACK</span>
              <strong>{result.predicted_attack}</strong>
            </div>

            <div className="summary-item">
              <span>CLASS ID</span>
              <strong>
                #{result.predicted_class_id}
              </strong>
            </div>

            <div className="summary-item">
              <span>CONFIDENCE</span>
              <strong>
                {(result.confidence * 100).toFixed(2)}%
              </strong>
            </div>

            <div className="summary-item">
              <span>RECORDS ANALYZED</span>
              <strong>5</strong>
            </div>

            <div className="summary-item">
              <span>FEATURES ANALYZED</span>
              <strong>39</strong>
            </div>

            <div className="summary-item">
              <span>EXPLAINABILITY</span>
              <strong>SHAP</strong>
            </div>

          </div>

        </div>
      )}

    </section>
  );
}

export default TrafficAnalysis;