import React from "react";
import { Link } from "react-router-dom";
import "./LandingPage.css"; // Import custom CSS

function LandingPage() {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <div className="hero-section">
        <h1>Welcome to Document Management and Q&A</h1>
        <p className="lead">
          A powerful tool to manage your documents and get answers to your
          questions using advanced AI.
        </p>
        <div className="cta-buttons">
          <Link to="/ingest" className="btn btn-primary btn-lg">
            Ingest Documents
          </Link>
          <Link to="/qa" className="btn btn-outline-light btn-lg">
            Ask a Question
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="features-section">
        <h2>Features</h2>
        <div className="features-grid">
          <div className="feature-card">
            <h3>Document Ingestion</h3>
            <p>
              Upload and store your documents securely. Generate embeddings for
              efficient retrieval.
            </p>
          </div>
          <div className="feature-card">
            <h3>Retrieval-Augmented Q&A</h3>
            <p>
              Ask questions and get accurate answers based on the content of your
              documents.
            </p>
          </div>
          <div className="feature-card">
            <h3>Easy to Use</h3>
            <p>
              A user-friendly interface designed for seamless document management
              and Q&A.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;