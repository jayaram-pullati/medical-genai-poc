import boto3
from app.config import settings

class DynamoDBAdapter:
    def __init__(self):
        self.ddb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
        self.table = self.ddb.Table(settings.DDB_TABLE)

    def get_drug_metadata(self, drug_id: str) -> dict | None:
        resp = self.table.get_item(Key={"drugId": drug_id})
        return resp.get("Item")
