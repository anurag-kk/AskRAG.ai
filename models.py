from sqlalchemy import create_engine, Column, Integer, String, Text, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os

# Create the base class for SQLAlchemy models
Base = declarative_base()

# Database URL (replace with your actual credentials)
DATABASE_URL = os.get_env('DATABASE_URL')
engine = create_engine(DATABASE_URL)

# Document model
class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)  # Title cannot be null

    # Relationship to chunks
    chunks = relationship("DocumentChunk", backref="document", cascade="all, delete-orphan")

# DocumentChunk model
class DocumentChunk(Base):
    __tablename__ = "document_chunks"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # Use Text for large content
    embedding = Column(LargeBinary, nullable=False)  # Embedding cannot be null
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)  # Link to Document

# Create all tables in the database
Base.metadata.create_all(bind=engine)