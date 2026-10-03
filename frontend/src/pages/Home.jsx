import React from "react";

export default function Home() {
  return (
    <section className="hero">
      <div className="hero-inner">
        <div className="hero-left">
          <h1 className="hero-title">Welcome to <span className="accent">AutoMLStudio</span></h1>
          <p className="hero-sub">
            A streamlined platform to explore datasets, extract insights and build reliable ML pipelines.
            Fast previews, one-click preprocessing, and clear visualizations — built for data scientists & product teams.
          </p>

          <div className="hero-ctas">
            <a
              className="btn primary large"
              href="http://127.0.0.1:5000"
              target="_blank"
              rel="noreferrer"
            >
              Step 1 — Dataset Insights
            </a>
            <a
              className="btn ghost large"
              href="http://127.0.0.1:5001"
              target="_blank"
              rel="noreferrer"
            >
              Step 2 — Data Preprocessing
            </a>
          </div>

          <ul className="features">
            <li><strong>Quick EDA:</strong> automatic summaries and visual overviews</li>
            <li><strong>Smart Preprocessing:</strong> missing values, encodings & scaling templates</li>
            <li><strong>Model Ready:</strong> export cleaned data / preview model inputs</li>
          </ul>
        </div>

        <div className="hero-right">
          <div className="card">
            <h3>Project status</h3>
            <p>Connected to local Flask services for Step 1 & Step 2. Use the above buttons to open them.</p>
            <div className="meta-row">
              <div><strong>Datasets:</strong> CSV, Excel</div>
              <div><strong>Output:</strong> Clean CSV / JSON</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
