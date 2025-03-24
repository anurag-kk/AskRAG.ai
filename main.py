from fastapi import FastAPI, Depends, HTTPException
from models import Document
from schemas import DocumentIn, QuestionIn
from services import ingest_document, retrieve_answer, select_documents
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File, Form
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ask-rag-ai.vercel.app"],  # Allow requests from the frontend
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/documents/")
def get_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).all()
    return [
        {
            "id": doc.id,
            "title": doc.title,
            "num_chunks": len(doc.chunks),  # Optional: Include the number of chunks
        }
        for doc in documents
    ]

@app.get("/documents/{document_id}/chunks/")
def get_document_chunks(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return [
        {
            "id": chunk.id,
            "content": chunk.content,
            "embedding": chunk.embedding,  # Optional: Include embeddings if needed
        }
        for chunk in document.chunks
    ]

@app.post("/ingest/")
async def ingest(
    title: str = Form(...),  # Required field from FormData
    content: str = Form(None),  # Optional field from FormData
    file: Optional[UploadFile] = File(None),  # Optional file from FormData
    db: Session = Depends(get_db)
):
    # Create a DocumentIn object manually
    doc = DocumentIn(title=title, content=content, file=file)
    
    # Call the ingest_document function
    return ingest_document(db, doc, file)

@app.post("/qa/")
async def qa(question: QuestionIn, db: Session = Depends(get_db)):
    return retrieve_answer(db, question.question)

@app.post("/select-documents/")
async def select(doc_ids: list[int], db: Session = Depends(get_db)):
    return select_documents(db, doc_ids)