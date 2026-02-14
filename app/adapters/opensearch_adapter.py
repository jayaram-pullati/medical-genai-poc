from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from app.config import settings

class OpenSearchAdapter:
    def __init__(self):
        session = boto3.Session()
        creds = session.get_credentials().get_frozen_credentials()
        awsauth = AWS4Auth(creds.access_key, creds.secret_key, settings.AWS_REGION, "es", session_token=creds.token)

        self.client = OpenSearch(
            hosts=[{"host": settings.OPENSEARCH_HOST.replace("https://", "").replace("http://", ""), "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
        )

    def knn_search(self, query_vector: list[float], k: int = 5, filter_latest: bool = True) -> list[dict]:
        """
        Retrieve top-k chunks using vector similarity.
        Assumes the index has a 'vector' field and metadata like 'doc_version' or 'effective_date'.
        """
        query = {
            "size": k,
            "query": {
                "knn": {
                    "vector": {
                        "vector": query_vector,
                        "k": k
                    }
                }
            }
        }

        # Optional: filter only latest/approved documents (recommended for medical content)
        # This requires your documents to store metadata fields.
        if filter_latest:
            query = {
                "size": k,
                "query": {
                    "bool": {
                        "must": [
                            {"knn": {"vector": {"vector": query_vector, "k": k}}}
                        ],
                        "filter": [
                            {"term": {"approved": True}}
                        ]
                    }
                }
            }

        resp = self.client.search(index=settings.OPENSEARCH_INDEX, body=query)
        hits = resp["hits"]["hits"]

        results = []
        for h in hits:
            src = h["_source"]
            results.append({
                "doc_id": src.get("doc_id"),
                "chunk_id": src.get("chunk_id"),
                "text": src.get("text"),
                "score": h.get("_score"),
            })
        return results
