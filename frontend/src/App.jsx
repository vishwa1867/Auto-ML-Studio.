import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Visualization from "./pages/Visualization";
import DatasetInsights from "./pages/DatasetInsights";
import "./App.css";

export default function App() {
  const openFlaskApp = () => {
    window.open("http://127.0.0.1:5000", "_blank");
  };

  const openPreprocessingApp = () => {
    window.open("http://127.0.0.1:5001", "_blank");
  };

  return (
    <BrowserRouter>
      {/* BACKGROUND VIDEO */}
      <video className="bg-video" autoPlay loop muted>
        <source src="bg2.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      {/* NAVBAR (always full width) */}
      <nav className="navbar">
        <div className="nav-logo">⚡ AutoML Studio</div>
        <div className="nav-links">
          <Link to="/visualization">Visualization</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
          <Link to="/insights">Insights</Link>
        </div>
        <div className="nav-buttons">
          <button onClick={openFlaskApp} className="btn-gradient">
            Step 1: Dataset Insights
          </button>
          <button onClick={openPreprocessingApp} className="btn-gradient">
            Step 2: Preprocessing
          </button>
        </div>
      </nav>

      {/* HERO SECTION */}
      <div className="hero">
        <div className="hero-box">
          <h1 className="hero-title">
            Welcome to <span>AutoML Studio</span>
          </h1>
          <p className="hero-subtitle">
            A streamlined platform to explore datasets, extract insights, and build reliable ML pipelines.
            Fast previews, one-click preprocessing, and clear visualizations — built for data scientists & product teams.
          </p>

          <div className="hero-actions">
            <button onClick={openFlaskApp} className="btn-gradient">
              🚀 Step 1: Dataset Insights
            </button>
            <button onClick={openPreprocessingApp} className="btn-gradient">
              ⚡ Step 2: Data Preprocessing
            </button>
          </div>

          <div className="features">
            <div className="feature-card">
              📊 <h3>Quick EDA</h3>
              <p>Automatic summaries and dataset visualizations.</p>
            </div>
            <div className="feature-card">
              ⚙️ <h3>Smart Preprocessing</h3>
              <p>Handle missing values, encodings, and scaling templates.</p>
            </div>
            <div className="feature-card">
              📈 <h3>Model Ready</h3>
              <p>Export cleaned datasets & preview model inputs instantly.</p>
            </div>
            <div className="feature-card">
              🤖 <h3>Automation</h3>
              <p>Focus on insights while AutoML takes care of the workflow.</p>
            </div>            
          </div>
        </div>
      </div>

      {/* ROUTES */}
      <Routes>
        <Route path="/visualization" element={<Visualization />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/insights" element={<DatasetInsights />} />
      </Routes>
    </BrowserRouter>
  );
}
