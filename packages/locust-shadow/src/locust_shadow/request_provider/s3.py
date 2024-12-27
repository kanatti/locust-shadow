import json
import boto3
from botocore.exceptions import ClientError
from .base import BaseRequestProvider

class S3RequestProvider(BaseRequestProvider):
    def __init__(self, bucket_name: str, object_key: str, endpoint_url: str = None):
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.s3_client = boto3.client('s3', endpoint_url=endpoint_url)
        self.requests = []

    def get_request(self):
        if not self.requests:
            self.load_requests()
        return self.requests.pop(0) if self.requests else None

    def load_requests(self):
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=self.object_key)
            content = response['Body'].read().decode('utf-8')
            self.requests = [json.loads(line) for line in content.splitlines()]
        except ClientError as e:
            print(f"Error loading requests from S3: {e}")
            self.requests = []