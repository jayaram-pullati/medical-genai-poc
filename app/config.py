import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

    S3_BUCKET = os.getenv("S3_BUCKET", "")
    DDB_TABLE = os.getenv("DDB_TABLE", "")

    OPENSEARCH_HOST = os.getenv("OPENSEARCH_HOST", "")
    OPENSEARCH_INDEX = os.getenv("OPENSEARCH_INDEX", "drug_chunks")

    BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "")
    BEDROCK_EMBED_MODEL_ID = os.getenv("BEDROCK_EMBED_MODEL_ID", "")

settings = Settings()
