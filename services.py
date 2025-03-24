from transformers import AutoTokenizer, AutoModel
from typing import Optional
import torch
import numpy as np
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from models import Document, DocumentChunk
from database import SessionLocal
from schemas import DocumentIn
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline
from fastapi import UploadFile, File, HTTPException

from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
current_vector_store: Optional[FAISS] = None

def create_llm_pipeline():
    # Use an instruction-tuned model (e.g., Flan-T5)
    model_name = "google/flan-t5-large"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    text_generation_pipeline = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=50,  # Limit answer length
        temperature=0.1,    # Reduce randomness
    )

    return HuggingFacePipeline(pipeline=text_generation_pipeline)

# Initialize text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,  # Number of tokens per chunk
    chunk_overlap=50,  # Overlap between chunks to preserve context
    length_function=len,  # Function to measure text length
)

def generate_embeddings(text: str):
    print("Generating embeddings for text...")
    tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
    model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    # Tokenize and generate embeddings
    print(f"Tokenizing text (length: {len(text)})...")
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        print("Generating embeddings...")
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).numpy()
    print("Embeddings generated successfully.")
    return embeddings

def ingest_document(db: SessionLocal, doc: DocumentIn, file: UploadFile = File(None)):
    print(f"Ingesting document: {doc.title}")

    # If a file is provided, read its content
    if file:
        print(f"Processing file: {file.filename}")
        content = ""
        if file.filename.endswith(".txt"):
            # Read text file
            content = file.file.read().decode("utf-8")
        elif file.filename.endswith(".pdf"):
            # Read PDF file
            pdf_reader = PyPDF2.PdfReader(file.file)
            for page in pdf_reader.pages:
                content += page.extract_text()
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only .txt and .pdf files are allowed.")
    else:
        # Use the provided content if no file is uploaded
        if not doc.content:
            raise HTTPException(status_code=400, detail="Either content or a file must be provided.")
        content = doc.content

    # Create a new Document entry for the whole document
    db_document = Document(title=doc.title)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    # Split the document into chunks
    print("Splitting document into chunks...")
    chunks = text_splitter.split_text(content)
    print(f"Document split into {len(chunks)} chunks.")

    # Generate embeddings for each chunk and store in the database
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        embeddings = generate_embeddings(chunk)
        db_chunk = DocumentChunk(content=chunk, embedding=embeddings.tobytes(), document_id=db_document.id)
        db.add(db_chunk)

    db.commit()
    print("Document ingestion completed successfully.")
    return {"message": f"Ingested {len(chunks)} chunks from the document"}

def retrieve_answer(db: SessionLocal, question: str):
    global current_vector_store  # Access the global variable

    print(f"Retrieving answer for question: {question}")
    
    # Use the current vector store if it exists; otherwise, use all chunks
    if current_vector_store is None:
        print("No documents selected. Using all chunks.")
        # Retrieve all document chunks from the database
        chunks = db.query(DocumentChunk).all()
        texts = [chunk.content for chunk in chunks]
        embeddings = [np.frombuffer(chunk.embedding, dtype=np.float32) for chunk in chunks]

        # Create a FAISS vector store
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        current_vector_store = FAISS.from_texts(texts, embedding_model)
    else:
        print("Using selected documents.")

    # Retrieve the most relevant document chunks
    print("Retrieving relevant document chunks...")
    retriever = current_vector_store.as_retriever(search_kwargs={"k": 2})  # Retrieve top 2 chunks
    relevant_docs = retriever.get_relevant_documents(question)
    print(f"Retrieved {len(relevant_docs)} relevant chunks.")

    # Combine the relevant chunks into a single context
    context = "\n".join([doc.page_content for doc in relevant_docs])
    print(f"Combined context: {context}")

    # Create a prompt for the language model
    prompt = f"""
    ### INSTRUCTION ###
    Answer the question based on the context below. Be concise and factual. Do NOT repeat the question or context.

    ### CONTEXT ###
    {context}

    ### QUESTION ###
    {question}

    ### ANSWER ###
    """

    # Generate the answer
    llm = create_llm_pipeline()
    answer = llm(prompt)
    print(f"Answer generated: {answer}")

    return {"question": question, "answer": answer}

def select_documents(db: SessionLocal, doc_ids: list[int]):
    global current_vector_store  # Access the global variable

    print(f"Selecting documents with IDs: {doc_ids}")
    
    # Retrieve selected documents from the database
    print("Fetching selected documents from the database...")
    selected_docs = db.query(Document).filter(Document.id.in_(doc_ids)).all()
    print(f"Found {len(selected_docs)} selected documents.")

    # Retrieve all chunks belonging to the selected documents
    selected_chunks = []
    for doc in selected_docs:
        chunks = db.query(DocumentChunk).filter(DocumentChunk.document_id == doc.id).all()
        selected_chunks.extend(chunks)

    texts = [chunk.content for chunk in selected_chunks]
    embeddings = [np.frombuffer(chunk.embedding, dtype=np.float32) for chunk in selected_chunks]

    # Recreate the FAISS vector store with selected chunks
    print("Recreating FAISS vector store with selected chunks...")
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    current_vector_store = FAISS.from_texts(texts, embedding_model)  # Update the global variable
    print("FAISS vector store recreated successfully.")
    
    return {"message": f"Selected {len(selected_chunks)} chunks for Q&A"}