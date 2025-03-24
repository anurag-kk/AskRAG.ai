import React, { useState } from "react";
import axios from "axios";
import "./DocumentIngestion.css";

function DocumentIngestion() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [file, setFile] = useState(null);

  const handleIngest = async (e) => {
    e.preventDefault();
  
    const formData = new FormData();
    formData.append("title", title);
    if (content) formData.append("content", content);
    if (file) formData.append("file", file);
  
    try {
      console.log(formData)
      const response = await axios.post("http://127.0.0.1:8000/ingest/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      alert(response.data.message);
      setTitle("");
      setContent("");
      setFile(null);
    } catch (error) {
      console.error("Error ingesting document:", error);
      alert("Failed to ingest document. Please try again.");
    }
  };

  return (
    <div className="card ingestion-card">
      <div className="card-body">
        <h2>Ingest Document</h2>
        <form onSubmit={handleIngest}>
          <div className="mb-3">
            <label htmlFor="title" className="form-label">
              Title
            </label>
            <input
              type="text"
              className="form-control"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="content" className="form-label">
              Content (Optional)
            </label>
            <textarea
              className="form-control"
              id="content"
              rows="5"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
          </div>
          <div className="mb-3">
            <label htmlFor="file" className="form-label">
              Upload File (Optional)
            </label>
            <input
              type="file"
              className="form-control"
              id="file"
              onChange={(e) => setFile(e.target.files[0])}
              accept=".txt,.pdf"
            />
          </div>
          <button type="submit" className="btn btn-primary ingest-button">
            Ingest Document
          </button>
        </form>
      </div>
    </div>
  );
}

export default DocumentIngestion;