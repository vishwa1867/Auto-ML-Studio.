import React, { useState } from "react";
import axios from "axios";

function Output({ cleanedPath }) {
  const [modelChoice, setModelChoice] = useState("");
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleTrain = async () => {
    if (!modelChoice) {
      alert("Select a model first!");
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post("http://localhost:5001/train-model", {
        file_path: cleanedPath,
        model_choice: modelChoice,
      });
      setMetrics(response.data);
    } catch (err) {
      console.error(err);
      alert("Error training model. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ marginTop: "30px" }}>
      <h2>Step 3: Train Model</h2>

      <div>
        <label>Select Model: </label>
        <select
          value={modelChoice}
          onChange={(e) => setModelChoice(e.target.value)}
        >
          <option value="">-- Choose Model --</option>
          <option>Random Forest</option>
          <option>Decision Tree</option>
          <option>XGBoost</option>
          <option>Logistic Regression</option>
          <option>SVM</option>
        </select>
        <button onClick={handleTrain} style={{ marginLeft: "10px" }}>
          Run Model
        </button>
      </div>

      {loading && <p>⚡ Training model...</p>}

      {metrics && (
        <div style={{ marginTop: "20px" }}>
          <h3>Model Metrics</h3>
          <p>Model: {metrics.Model}</p>
          <p>Accuracy: {metrics["Accuracy"]}</p>
          <p>F1 Score: {metrics["F1 Score"]}</p>
        </div>
      )}
    </div>
  );
}

export default Output;
