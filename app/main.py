from fastapi import FastAPI
from pydantic import BaseModel
from app.services.rag_service import RAGService

app = FastAPI(title="Medical GenAI POC")
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = RAGService()

class AskRequest(BaseModel):
    question: str

@app.get("/")
def health():
    return {"message": "Medical GenAI POC is running"}

@app.post("/ask")
def ask(req: AskRequest):
    # This calls Bedrock embeddings + OpenSearch kNN + Bedrock generation
    return rag.answer(req.question)
