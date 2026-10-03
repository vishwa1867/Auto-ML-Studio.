import React from "react";

export default function Visualization() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>NN Pipeline Visualization</h1>
      <p>A high-level view of the end-to-end system.</p>

      {/* Pipeline Flow */}
      <div style={{ display: "flex", alignItems: "center", margin: "20px 0" }}>
        <div style={{ textAlign: "center" }}>
          <h2>📂</h2>
          <p>User Input</p>
          <small>Upload dataset or describe the problem. Choose task, constraints.</small>
        </div>
        <span style={{ margin: "0 15px" }}>→</span>
        <div style={{ textAlign: "center" }}>
          <h2>🤖</h2>
          <p>Decision (GPT-4)</p>
          <small>Analyze requirement. Pick Existing CNN template or Create Custom NN.</small>
        </div>
        <span style={{ margin: "0 15px" }}>→</span>
        <div style={{ textAlign: "center" }}>
          <h2>📓</h2>
          <p>Notebook Customization</p>
          <small>Edit .ipynb cells: preprocessing, layers, hyperparams, device.</small>
        </div>
        <span style={{ margin: "0 15px" }}>→</span>
        <div style={{ textAlign: "center" }}>
          <h2>⚙️</h2>
          <p>Training</p>
          <small>Run training with chosen architecture & resources.</small>
        </div>
        <span style={{ margin: "0 15px" }}>→</span>
        <div style={{ textAlign: "center" }}>
          <h2>📊</h2>
          <p>Visualization & Output</p>
          <small>Show metrics, curves, and best model recommendation.</small>
        </div>
      </div>

      {/* Quick Actions */}
      <h3>Quick Actions</h3>
      <button style={{ margin: "5px" }}>Analyze Dataset (coming next)</button>
      <button style={{ margin: "5px" }}>Select Template (coming next)</button>
      <button style={{ margin: "5px" }}>Generate Notebook (coming next)</button>

      {/* Status */}
      <h3>Status</h3>
      <p>Dataset: —</p>
      <p>Decision: —</p>
      <p>Template/Model: —</p>
      <p>ETA: —</p>

      <small>
        Next: we’ll wire these buttons to backend endpoints to analyze the dataset, pick a template/custom NN,
        generate a tailored notebook, and show a training ETA with progress.
      </small>
    </div>
  );
}
