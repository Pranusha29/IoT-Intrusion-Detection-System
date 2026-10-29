import "./App.css";
import TrafficAnalysis from "./components/TrafficAnalysis";

function App() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">◈</div>
          <div>
            <h2>IoT-IDS</h2>
            <span>AI Security System</span>
          </div>
        </div>

        <nav>
        <button
  className="nav-item"
  onClick={() =>
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    })
  }
>
  <span>⌂</span>
  Dashboard
</button>

<button
  className="nav-item"
  onClick={() =>
    document
      .getElementById("traffic-analysis")
      ?.scrollIntoView({ behavior: "smooth" })
  }
>
  <span>◉</span>
  Traffic Analysis
</button>

<button
  className="nav-item"
  onClick={() =>
    document
      .getElementById("attack-detection")
      ?.scrollIntoView({ behavior: "smooth" })
  }
>
  <span>⚠</span>
  Attack Detection
</button>

<button
  className="nav-item"
  onClick={() =>
  document
    .querySelector(".shap-results-card")
    ?.scrollIntoView({ behavior: "smooth" })
}
>
  <span>▣</span>
  Model Insights
</button>

<button
  className="nav-item"
  onClick={() =>
  document
    .querySelector(".prediction-summary-card")
    ?.scrollIntoView({ behavior: "smooth" })
}
>
  <span>◌</span>
  Explainability
</button>
        </nav>

        <div className="sidebar-bottom">
          <div className="api-status">
            <span className="status-dot"></span>
            <div>
              <strong>API Online</strong>
              <small>localhost:5000</small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">INTRUSION DETECTION PLATFORM</p>
            <h1>Security Dashboard</h1>
          </div>

          <div className="model-badge">
            <span className="pulse"></span>
            CNN · LSTM · Attention
          </div>
        </header>

        <section className="hero">
          <div className="hero-content">
            <span className="hero-tag">AI-POWERED NETWORK SECURITY</span>

            <h2>
              Detect IoT attacks
              <br />
              <span>before they become threats.</span>
            </h2>

            <p>
              Analyze network traffic using a hybrid CNN-LSTM-Attention
              architecture and identify suspicious IoT activity across
              34 attack classes.
            </p>

            <div className="hero-actions">
              <button className="primary-btn">
                Analyze Traffic →
              </button>

              <button className="secondary-btn">
                View Model
              </button>
            </div>
          </div>

          <div className="network-visual">
            <div className="orbit orbit-one"></div>
            <div className="orbit orbit-two"></div>
            <div className="core">
              <div className="core-inner">AI</div>
            </div>

            <div className="node node-one">IoT</div>
            <div className="node node-two">CNN</div>
            <div className="node node-three">LSTM</div>
            <div className="node node-four">SHAP</div>
          </div>
        </section>

        <section className="stats-grid">

  <div className="stat-card">
    <span className="stat-label">MODEL ACCURACY</span>
    <strong>77.34%</strong>
    <small>Test accuracy</small>
  </div>


  <div className="stat-card">
    <span className="stat-label">FEATURES</span>
    <strong>39</strong>
    <small>Network Traffic Features</small>
  </div>

  <div className="stat-card">
    <span className="stat-label">ATTACK CLASSES</span>
    <strong>34</strong>
    <small>Fine-Grained Classes</small>
  </div>

  <div className="stat-card">
    <span className="stat-label">WINDOW SIZE</span>
    <strong>5</strong>
    <small>Traffic Records</small>
  </div>

  

</section>

      
        <div id="traffic-analysis">
            <TrafficAnalysis />
        </div>

        <footer>
          <span>IoT Intrusion Detection System</span>
          <span>CICIoT2023 · CNN-LSTM-Attention · SHAP</span>
        </footer>
      </main>
    </div>
  );
}

export default App;