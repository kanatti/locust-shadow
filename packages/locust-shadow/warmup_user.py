import json
import time
from locust import HttpUser, task, constant_throughput, events
import gevent
import random
import logging

class WarmupUser(HttpUser):
    wait_time = constant_throughput(1)  # This will be updated in increase_rps_periodically

    def __init__(self, environment):
        super().__init__(environment)
        self.warmup_config = None
        self.requests = []
        self.current_rps = 0
        self.start_time = None

    def on_start(self):
        self.warmup_config = self.environment.runner.warmup_config
        self.load_requests()
        self.start_time = time.time()

        logging.info(f"Starting warmup with initial RPS: {self.warmup_config.start_rps}")
        logging.info(f"Step duration: {self.warmup_config.step_duration} seconds")
        logging.info(f"RPS increment: {self.warmup_config.rps_increment}")
        logging.info(f"Target RPS: {self.warmup_config.end_rps}")

        # Set initial wait_time
        self.wait_time = constant_throughput(self.warmup_config.start_rps)
        self.wait_time = self.wait_time.__get__(self, WarmupUser)  # Bind the method to the instance

        gevent.spawn(self.increase_rps_periodically)

    def load_requests(self):
        for request_file in self.warmup_config.request_files:
            with open(request_file, "r") as f:
                self.requests.extend([json.loads(line) for line in f])
        if not self.requests:
            raise ValueError("No requests found in the JSONL files")
        logging.info(f"Loaded {len(self.requests)} requests from JSONL files")

    def increase_rps_periodically(self):
        self.current_rps = self.warmup_config.start_rps
        step_count = 0

        while self.current_rps < self.warmup_config.end_rps:
            gevent.sleep(self.warmup_config.step_duration)
            step_count += 1
            self.current_rps = min(self.warmup_config.start_rps + step_count * self.warmup_config.rps_increment, 
                                   self.warmup_config.end_rps)
            self.wait_time = constant_throughput(self.current_rps)
            self.wait_time = self.wait_time.__get__(self, WarmupUser)  # Bind the method to the instance
            logging.info(f"Step {step_count}: Increased RPS to {self.current_rps}")

        logging.info(f"Warmup complete. Reached target RPS of {self.current_rps}")


    @task
    def execute_request(self):
        if self.current_rps >= self.warmup_config.end_rps:
            logging.info("Reached or exceeded target RPS. Stopping the test.")
            self.environment.runner.quit()
            return

        request = random.choice(self.requests)
        self.client.get(request["path"], params=request["params"])
