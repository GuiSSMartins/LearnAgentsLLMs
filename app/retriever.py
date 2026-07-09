"""
Document retrieval abstraction.
"""

from typing import List

from app.config import settings
from app.database import get_database
from app.models import RetrievedDocument


class Retriever:

    def __init__(self,
        top_k: int | None = None
    ):
        #self.db = get_database()
        self.top_k = top_k or settings.TOP_K

    def _retrieve(self, question):
        db = get_database()
        return db.similarity_search_with_score(
            question,
            k=self.top_k
        )
    
    def _convert(self, results):
        documents = []
        for rank, (doc, score) in enumerate(results, start=1):
            documents.append(
                RetrievedDocument(
                    document=doc,
                    score=float(score),
                    rank=rank
                )
            )
        return documents
    
    def search(self, question: str
    ) -> List[RetrievedDocument]:
        """
        Retrieve the most relevant documents.
        """
        raw_results = self._retrieve(question)
        return self._convert(raw_results)