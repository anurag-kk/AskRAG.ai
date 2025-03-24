# AskRAG.ai

Check out the website --> [AskRAG.ai](https://ask-rag-ai.vercel.app/) <--

# AskRAG.ai - Retrieval-Augmented Generation (RAG) Question-Answering Application

AskRAG.ai is a scalable and efficient Retrieval-Augmented Generation (RAG) question-answering application. It combines the power of **retrieval-based** and **generative** models to provide accurate and contextually relevant answers to user queries. This application is designed with scalability, efficiency, and proper error handling in mind.

---

## Features

1. **Document Ingestion**:
   - Upload documents (PDF or text files) or provide text content directly.
   - Documents are split into chunks, and embeddings are generated for each chunk using a state-of-the-art embedding model.
   - Chunks and embeddings are stored in a PostgreSQL database for efficient retrieval.

2. **Question-Answering**:
   - Users can ask questions, and the system retrieves the most relevant document chunks using **FAISS** (Facebook AI Similarity Search).
   - A generative model synthesizes the answer based on the retrieved context.

3. **Scalability**:
   - The application is designed to handle large volumes of documents and queries efficiently.
   - The use of FAISS ensures fast and accurate retrieval of relevant chunks.

4. **Error Handling and Logging**:
   - Proper error handling is implemented to ensure robustness.
   - Logging is used to track application behavior and debug issues.

5. **Frontend**:
   - A user-friendly web interface built with **React** allows users to upload documents, ask questions, and view answers.

---

## How It Works

### 1. Document Ingestion
- Users upload documents (PDF or text files) or provide text content.
- The backend processes the documents:
  - Splits the content into manageable chunks.
  - Generates embeddings for each chunk using the **sentence-transformers/all-MiniLM-L6-v2** model.
  - Stores the chunks and embeddings in a PostgreSQL database.

### 2. Question-Answering
- Users submit a question through the frontend.
- The backend:
  - Retrieves the most relevant document chunks using FAISS.
  - Combines the retrieved chunks into a context.
  - Generates an answer using a generative model (e.g., GPT-based models).
 
### 3. Document Selection
- Users can select the particular documents from which they want to query
- The backend:
  - Queries the database to retrieve chunks from the selected documents.
  - Retrieves the relavent chunks using FAISS

### 3. Scalability and Efficiency
- **FAISS** is used for fast and efficient similarity search, enabling the application to handle large datasets.
- The use of **chunking** ensures that large documents are processed efficiently.

---

## Design Choices

### 1. Retrieval Algorithms
- **FAISS**: Chosen for its efficiency and scalability in similarity search. It allows for fast retrieval of relevant document chunks, even with large datasets.

### 2. Embedding Models
- **sentence-transformers/all-MiniLM-L6-v2**: Chosen for its balance between accuracy and efficiency. It generates high-quality embeddings suitable for semantic search.

### 3. Database
- **PostgreSQL**: Used to store document metadata and chunk embeddings. PostgreSQL is reliable, scalable, and supports complex queries.

### 4. Error Handling and Logging
- Proper error handling ensures that the application gracefully handles unexpected issues.
- Logging is implemented to track application behavior, making it easier to debug and monitor.

![Home Page](/Home.png)
![Ingest Document](/Ingest.png)
![Document Selection & QA](/QA.png)



