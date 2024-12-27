import json
import random
from typing import List
from locust_shadow.request_provider.base import BaseRequestProvider

class FileRequestProvider(BaseRequestProvider):
    def __init__(self, request_files: List[str]):
        self.request_files = request_files
        self.requests = []
        self.load_requests()

    def get_request(self):
        return random.choice(self.requests)

    def load_requests(self):
        for request_file in self.request_files:
            with open(request_file, "r") as f:
                self.requests.extend([json.loads(line) for line in f])
        if not self.requests:
            raise ValueError("No requests found in the JSONL files")
