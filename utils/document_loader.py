from pathlib import Path
from typing import List

from langchain_core.documents import Document


def load_financial_documents(docs_path: str) -> List[Document]:
    """Load TXT, MD, and PDF files from a directory."""
    path = Path(docs_path)
    documents: List[Document] = []

    if not path.exists():
        return documents

    for file_path in path.rglob("*"):
        if file_path.is_dir():
            continue

        suffix = file_path.suffix.lower()

        if suffix in [".txt", ".md"]:
            text = file_path.read_text(encoding="utf-8", errors="ignore")
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": str(file_path), "file_name": file_path.name},
                )
            )

        elif suffix == ".pdf":
            try:
                from pypdf import PdfReader

                reader = PdfReader(str(file_path))
                pdf_text = []
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text() or ""
                    pdf_text.append(text)

                documents.append(
                    Document(
                        page_content="\n".join(pdf_text),
                        metadata={"source": str(file_path), "file_name": file_path.name},
                    )
                )
            except Exception as exc:
                documents.append(
                    Document(
                        page_content=f"Failed to load PDF {file_path.name}: {exc}",
                        metadata={"source": str(file_path), "file_name": file_path.name},
                    )
                )

    return documents
