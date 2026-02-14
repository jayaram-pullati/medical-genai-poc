import json
import boto3
from app.config import settings

class BedrockAdapter:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=settings.AWS_REGION)

    def embed(self, text: str) -> list[float]:
        """
        Uses an embeddings model (e.g., Titan Embeddings) to produce a vector.
        Note: exact request/response shape depends on modelId.
        """
        body = {"inputText": text}
        resp = self.client.invoke_model(
            modelId=settings.BEDROCK_EMBED_MODEL_ID,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json",
        )
        payload = json.loads(resp["body"].read())
        return payload["embedding"]  # typical key for Titan embeddings

    def generate(self, question: str, context_chunks: list[dict]) -> str:
        """
        Generates an answer grounded only in context.
        This example shows a Claude-style prompt. Adjust if model differs.
        """
        context_text = "\n\n".join(
            [f"[{c['doc_id']}#{c['chunk_id']}] {c['text']}" for c in context_chunks]
        )

        prompt = f"""
You are a medical information assistant. Answer ONLY using the CONTEXT.
If the answer is not found in CONTEXT, say: "Not available in the provided source data."
Always keep the response factual and concise.

QUESTION:
{question}

CONTEXT:
{context_text}
""".strip()

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 400,
            "temperature": 0.1,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }

        resp = self.client.invoke_model(
            modelId=settings.BEDROCK_MODEL_ID,
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json",
        )
        payload = json.loads(resp["body"].read())

        # Claude responses typically appear in content[0].text
        return payload["content"][0]["text"]
