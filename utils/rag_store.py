from pathlib import Path
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.config_loader import load_config
from utils.document_loader import load_financial_documents


def _get_embeddings():
    """Return embeddings. Uses OpenAI if available; otherwise HuggingFace local embeddings."""
    import os

    if os.getenv("OPENAI_API_KEY"):
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model="text-embedding-3-small")

    from langchain_community.embeddings import HuggingFaceEmbeddings

    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def build_vector_store() -> str:
    """Build local FAISS vector store from financial documents."""
    from langchain_community.vectorstores import FAISS

    config = load_config()
    rag_config = config["rag"]

    docs_path = rag_config["docs_path"]
    vector_store_path = rag_config["vector_store_path"]
    chunk_size = rag_config.get("chunk_size", 1200)
    chunk_overlap = rag_config.get("chunk_overlap", 150)

    documents = load_financial_documents(docs_path)
    if not documents:
        return f"No documents found in {docs_path}. Add PDFs/TXT/MD files and run ingestion again."

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    chunks: List[Document] = splitter.split_documents(documents)

    embeddings = _get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)

    Path(vector_store_path).mkdir(parents=True, exist_ok=True)
    vector_store.save_local(vector_store_path)

    return f"Vector store created at {vector_store_path} with {len(chunks)} chunks."


def search_vector_store(question: str, k: int = 4) -> str:
    """Search local FAISS vector store."""
    from langchain_community.vectorstores import FAISS

    config = load_config()
    vector_store_path = config["rag"]["vector_store_path"]

    if not Path(vector_store_path).exists():
        return "Vector store not found. Run `python scripts/ingest_documents.py` first."

    embeddings = _get_embeddings()
    vector_store = FAISS.load_local(
        vector_store_path,
        embeddings,
        allow_dangerous_deserialization=True,
    )

    docs = vector_store.similarity_search(question, k=k)
    if not docs:
        return "No relevant document chunks found."

    lines = []
    for idx, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "unknown")
        text = doc.page_content[:1200]
        lines.append(f"Result {idx}\nSource: {source}\nContent:\n{text}")

    return "\n\n".join(lines)
