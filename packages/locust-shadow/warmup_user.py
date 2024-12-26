import json
from locust import HttpUser, task, between
import random
import logging

class WarmupUser(HttpUser):
    wait_time = between(0.1, 1)  # Small wait time between requests

    def __init__(self, environment):
        super().__init__(environment)
        self.warmup_config = None
        self.requests = []

    def on_start(self):
        self.warmup_config = self.environment.runner.warmup_config
        self.load_requests()

    def load_requests(self):
        for request_file in self.warmup_config.request_files:
            with open(request_file, "r") as f:
                self.requests.extend([json.loads(line) for line in f])
        if not self.requests:
            raise ValueError("No requests found in the JSONL files")
        logging.info(f"Loaded {len(self.requests)} requests from JSONL files")

    @task
    def execute_request(self):
        request = random.choice(self.requests)
        self.client.get(request["path"], params=request["params"])
