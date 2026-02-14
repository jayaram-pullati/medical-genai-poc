import boto3
from app.config import settings

class S3Adapter:
    def __init__(self):
        self.s3 = boto3.client("s3", region_name=settings.AWS_REGION)

    def read_text(self, key: str) -> str:
        obj = self.s3.get_object(Bucket=settings.S3_BUCKET, Key=key)
        return obj["Body"].read().decode("utf-8", errors="ignore")
