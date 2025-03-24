import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css"; // Import custom CSS
import LandingPage from "./components/LandingPage";
import DocumentIngestion from "./components/DocumentIngestion";
import DocumentSelectionQA from "./components/DocumentSelectionQA";

function App() {
  return (
    <Router>
      {/* Navigation Bar */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container">
          <Link className="navbar-brand" to="/">
            AskRAG.ai
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item">
                <Link className="nav-link" to="/">
                  Home
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/ingest">
                  Ingest Documents
                </Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/qa">
                  Q&A
                </Link>
              </li>
            </ul>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="container mt-4 main-content">
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/ingest" element={<DocumentIngestion />} />
          <Route path="/qa" element={<DocumentSelectionQA />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;