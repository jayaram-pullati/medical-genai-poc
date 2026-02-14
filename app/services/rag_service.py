import os
from app.adapters.bedrock_adapter import BedrockAdapter
from app.adapters.opensearch_adapter import OpenSearchAdapter

USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"


class RAGService:
    def __init__(self):
        if not USE_MOCK:
            self.bedrock = BedrockAdapter()
            self.search = OpenSearchAdapter()

    def answer(self, question: str) -> dict:
        # ✅ MOCK MODE (runs locally without AWS)
        if USE_MOCK:
            retrieved = [
                {
                    "doc_id": "drug-label-123",
                    "chunk_id": "warnings-07",
                    "text": "This medication may cause dizziness. Avoid driving until you know how it affects you.",
                    "score": 0.92,
                }
            ]
            answer_text = (
                "Based on the provided label, this medication may cause dizziness. "
                "Avoid driving until you understand how it affects you."
            )
            return {
                "question": question,
                "answer": answer_text,
                "citations": [{"doc_id": r["doc_id"], "chunk_id": r["chunk_id"]} for r in retrieved],
                "retrieved_context_preview": retrieved[0]["text"],
                "mode": "mock",
            }

        # ✅ REAL MODE (needs AWS creds + resources)
        qvec = self.bedrock.embed(question)
        chunks = self.search.knn_search(qvec, k=5, filter_latest=True)

        if not chunks:
            return {
                "question": question,
                "answer": "Not available in the provided source data.",
                "citations": [],
                "mode": "aws",
            }

        answer_text = self.bedrock.generate(question, chunks)
        citations = [{"doc_id": c["doc_id"], "chunk_id": c["chunk_id"]} for c in chunks]
        return {
            "question": question,
            "answer": answer_text,
            "citations": citations,
            "mode": "aws",
        }
