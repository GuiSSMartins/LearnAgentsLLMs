"""
Document loading utilities.

Responsible for:
- Loading supported document types
- Splitting documents into chunks
"""

from pathlib import Path
from typing import List
import json
import pandas as pd

from langchain_core.documents import Document

from langchain_community.document_loaders import (
    PyPDFDirectoryLoader,
    DirectoryLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    Docx2txtLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class DocumentLoader:

    def __init__(self):

        self.data_path = settings.DATA_PATH

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def load(self) -> List[Document]:
        """
        Load every supported document.
        """

        documents = []

        documents.extend(self._load_pdfs())
        documents.extend(self._load_txt())
        documents.extend(self._load_markdown())
        documents.extend(self._load_docx())
        documents.extend(self._load_html())
        documents.extend(self._load_csv())
        documents.extend(self._load_excel())
        documents.extend(self._load_json())

        return documents

    def split(
        self,
        documents: List[Document]
    ) -> List[Document]:

        return self.splitter.split_documents(documents)

    # ---------------------------------------------------------

    def _load_pdfs(self):

        folder = self.data_path / "pdf"
        if not folder.exists():
            return []

        loader = PyPDFDirectoryLoader(str(folder))

        return loader.load()

    # ---------------------------------------------------------

    def _load_txt(self):

        folder = self.data_path / "txt"
        if not folder.exists():
            return []

        loader = DirectoryLoader(
            str(folder),
            glob="**/*.txt",
            loader_cls=TextLoader
        )

        return loader.load()

    # ---------------------------------------------------------

    def _load_markdown(self):

        folder = self.data_path / "md"
        if not folder.exists():
            return []

        loader = DirectoryLoader(
            str(folder),
            glob="**/*.md",
            loader_cls=UnstructuredMarkdownLoader
        )

        return loader.load()

    # ---------------------------------------------------------

    def _load_docx(self):

        folder = self.data_path / "docx"
        if not folder.exists():
            return []

        loader = DirectoryLoader(
            str(folder),
            glob="**/*.docx",
            loader_cls=Docx2txtLoader
        )

        return loader.load()

    # ---------------------------------------------------------

    def _load_html(self):

        folder = self.data_path / "html"
        if not folder.exists():
            return []

        loader = DirectoryLoader(
            str(folder),
            glob="**/*.html",
            loader_cls=UnstructuredHTMLLoader
        )

        return loader.load()
    
    def _load_csv(self):

        folder = self.data_path / "csv"
        if not folder.exists():
            return []

        documents = []

        for file in folder.rglob("*.csv"):

            df = pd.read_csv(file)
            content = df.to_markdown(index=False)
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": str(file),
                        "type": "csv"
                    }
                )
            )

        return documents
    
    def _load_excel(self):

        folder = self.data_path / "excel"
        if not folder.exists():
            return []

        documents = []

        for file in folder.rglob("*.xlsx"):
            sheets = pd.read_excel(
                file,
                sheet_name=None
            )
            for sheet_name, df in sheets.items():
                content = df.to_markdown(index=False)
                documents.append(
                    Document(
                        page_content=content,
                        metadata={
                            "source": str(file),
                            "sheet": sheet_name,
                            "type": "excel"
                        }
                    )
                )

        return documents
    
    def _load_json(self):

        folder = self.data_path / "json"
        if not folder.exists():
            return []

        documents = []

        for file in folder.rglob("*.json"):
            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:
                data = json.load(f)

            content = json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )
            documents.append(
                Document(
                    page_content=content,
                    metadata={
                        "source": str(file),
                        "type": "json"
                    }
                )
            )

        return documents

    # ---------------------------------------------------------

    def _is_valid_file(path: Path) -> bool:
        return (
            path.is_file()
            and not path.name.startswith(".")
            and not path.name.startswith("~")
        )