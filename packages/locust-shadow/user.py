import json
import time
from locust import HttpUser, task, constant_throughput, events
import gevent


class DynamicMinuteBatchUser(HttpUser):
    def __init__(self, environment):
        super().__init__(environment)
        self.minute_batch = None
        self.requests = []
        self.request_index = 0
        self.rps = 1  # Default RPS
        self.start_time = time.time()

    def on_start(self):
        # Start a periodic updater
        gevent.spawn(self.update_minute_batch_periodically)

    def update_minute_batch_periodically(self):
        while True:
            self.update_minute_batch(self.environment.runner.minute_batches[self.environment.runner.current_minute])
            self.environment.runner.current_minute = (self.environment.runner.current_minute + 1) % len(self.environment.runner.minute_batches)
            gevent.sleep(60)

    def update_minute_batch(self, minute_batch):
        self.minute_batch = minute_batch
        self.rps = self.minute_batch.get("rps", 1)
        self.requests = []
        for request_file in self.minute_batch.get("request_files", []):
            with open(request_file, "r") as f:
                self.requests.extend([json.loads(line) for line in f])

        if not self.requests:
            raise ValueError("No requests found in the JSONL file")

        self.wait_time = constant_throughput(self.rps)  # Set the wait time to maintain RPS
        self.wait_time = self.wait_time.__get__(self, DynamicMinuteBatchUser)  # Bind the method to the instance
        self.request_index = 0

    @task
    def execute_request(self):
        if time.time() - self.start_time >= self.environment.runner.total_duration:
            self.environment.runner.quit()
            return

        if not self.minute_batch:
            return

        # If we've reached the end of the requests, loop back to the beginning
        if self.request_index >= len(self.requests):
            self.request_index = 0

        request = self.requests[self.request_index]
        self.client.get(request["path"], params=request["params"])
        self.request_index += 1
