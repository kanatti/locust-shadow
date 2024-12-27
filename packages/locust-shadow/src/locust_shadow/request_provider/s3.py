import json
import boto3
from botocore.exceptions import ClientError
from .base import BaseRequestProvider
from typing import List, Tuple

class S3RequestProvider(BaseRequestProvider):
    _session = None
    _client = None

    def __init__(self, s3_files: List[Tuple[str, str]], endpoint_url: str = None, profile: str = None):
        self.s3_files = s3_files
        self.s3_client = self.get_s3_client(endpoint_url, profile)
        self.requests = []
    
    @classmethod
    def get_s3_client(cls, endpoint_url: str = None, profile: str = None):
        if cls._client is None:
            if cls._session is None:
                cls._session = boto3.Session(profile_name=profile)
            cls._client = cls._session.client('s3', endpoint_url=endpoint_url)
        return cls._client

    def get_request(self):
        if not self.requests:
            self.load_requests()
        return self.requests.pop(0) if self.requests else None

    def load_requests(self):
        for bucket, key in self.s3_files:
            try:
                response = self.s3_client.get_object(Bucket=bucket, Key=key)
                content = response['Body'].read().decode('utf-8')
                self.requests.extend([json.loads(line) for line in content.splitlines()])
            except ClientError as e:
                print(f"Error loading requests from S3 (bucket: {bucket}, key: {key}): {e}")