import React, { useState, useEffect } from "react";
import axios from "axios";
import "./DocumentSelectionQA.css"; // Import custom CSS

function DocumentSelectionQA() {
  const [documents, setDocuments] = useState([]);
  const [selectedDocs, setSelectedDocs] = useState([]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // Fetch all documents on component mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  // Fetch documents from the backend
  const fetchDocuments = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/documents/");
      setDocuments(response.data);
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

  // Handle document selection
  const handleSelect = (docId) => {
    if (selectedDocs.includes(docId)) {
      setSelectedDocs(selectedDocs.filter((id) => id !== docId));
    } else {
      setSelectedDocs([...selectedDocs, docId]);
    }
  };

  // Handle "Select All" button
  const handleSelectAll = () => {
    if (selectedDocs.length === documents.length) {
      // If all documents are already selected, deselect all
      setSelectedDocs([]);
    } else {
      // Select all documents
      setSelectedDocs(documents.map((doc) => doc.id));
    }
  };

  // Handle Q&A
  const handleQA = async () => {
    if (selectedDocs.length === 0) {
      alert("Please select at least one document.");
      return;
    }

    try {
      // Select documents first
      await axios.post("http://127.0.0.1:8000/select-documents/", selectedDocs);

      // Ask the question
      const response = await axios.post("http://127.0.0.1:8000/qa/", {
        question,
      });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error("Error during Q&A:", error);
    }
  };

  return (
    <div className="document-selection-qa-container">
      {/* Sidebar for Document Selection */}
      <div className="sidebar">
        <h2>Select Documents</h2>
        <button className="select-all-button" onClick={handleSelectAll}>
          {selectedDocs.length === documents.length ? "Deselect All" : "Select All"}
        </button>
        <ul className="document-list">
          {documents.map((doc) => (
            <li key={doc.id} className="document-item">
              <input
                type="checkbox"
                checked={selectedDocs.includes(doc.id)}
                onChange={() => handleSelect(doc.id)}
                className="document-checkbox"
              />
              <label className="document-label">{doc.title}</label>
            </li>
          ))}
        </ul>
      </div>

      {/* Main Content for Chat Interface */}
      <div className="chat-interface">
        <h2>Chat</h2>
        <div className="chat-history">
          {answer && (
            <div className="answer-card">
              <h5>Answer:</h5>
              <p>{answer}</p>
            </div>
          )}
        </div>
        <div className="question-input-container">
          <div className="input-group">
            <input
              type="text"
              placeholder="Enter your question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="question-input"
            />
            <button className="ask-button" onClick={handleQA}>
              Ask
            </button>
          </div>
          {selectedDocs.length === 0 && (
            <div className="warning-message">
              No documents selected. Please select at least one document.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default DocumentSelectionQA;