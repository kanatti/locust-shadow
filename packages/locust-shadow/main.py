import json
import time
import os
from locust import HttpUser, task, constant_throughput
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent

class MinuteBatchUser(HttpUser):
    # Removed abstract = True as we're using this class directly
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = []
        self.request_index = 0
        self.rps = 1  # Default RPS
        self.start_time = None
        self.minute = 0

    def on_start(self):
        # Load manifest
        manifest_path = os.path.join("dev", "test_minute_batch", "manifest.json")
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        
        self.rps = manifest.get("rps", 1)  # Get RPS from manifest
        self.minute = manifest.get("minute", 0)  # Get minute from manifest

        # Load requests from the JSONL file
        jsonl_path = os.path.join("dev", "test_minute_batch", "requests1.jsonl")
        with open(jsonl_path, "r") as f:
            self.requests = [json.loads(line) for line in f]

        if not self.requests:
            raise ValueError("No requests found in the JSONL file")

        self.wait_time = constant_throughput(self.rps)  # Set the wait time to maintain RPS
        self.wait_time = self.wait_time.__get__(self, MinuteBatchUser)  # Bind the method to the instance
        self.start_time = time.time()

    @task
    def execute_request(self):
        if time.time() - self.start_time >= 60:
            self.environment.runner.quit()
            return

        # If we've reached the end of the requests, loop back to the beginning
        if self.request_index >= len(self.requests):
            self.request_index = 0

        request = self.requests[self.request_index]
        self.client.get(request["path"], params=request["params"])
        self.request_index += 1

def main():
    # Set up the Locust environment
    env = Environment(user_classes=[MinuteBatchUser], host="http://localhost:8000")
    env.create_local_runner()

    # Start the test
    env.runner.start(1, spawn_rate=1)

    # Setup logging and stats
    setup_logging("INFO", None)
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    # Wait for the test to finish
    env.runner.greenlet.join()

    # Stop the runner
    env.runner.quit()

if __name__ == "__main__":
    main()
