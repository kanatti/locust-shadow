import json
from locust import HttpUser, task, constant_throughput
import random
import logging

class WarmupUser(HttpUser):
    # We'll set this dynamically based on the current RPS and user count
    wait_time = constant_throughput(1)  # Default value, will be updated

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

    @classmethod
    def update_wait_time(cls, current_rps, user_count):
        if user_count > 0:
            # Calculate the required throughput per user
            throughput_per_user = current_rps / user_count
            cls.wait_time = constant_throughput(throughput_per_user)
        else:
            cls.wait_time = constant_throughput(1)  # Default to 1 RPS if user_count is 0
