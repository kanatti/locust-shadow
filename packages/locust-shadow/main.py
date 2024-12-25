import json
import time
import os
import argparse
from locust import HttpUser, task, constant_throughput, events
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
from config import Config
import logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="Locust Shadow - Replay production traffic patterns")
    parser.add_argument("config", help="Path to the config.yaml file")
    return parser.parse_args()

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

def main():
    args = parse_arguments()
    config = Config(args.config)
    minute_batches = config.get_minute_batches()

    # Calculate total duration
    total_duration = len(minute_batches) * 60

    # Set up the Locust environment
    env = Environment(user_classes=[DynamicMinuteBatchUser], host=config.get_host())
    env.create_local_runner()

    # Add minute_batches and total_duration to the runner
    env.runner.minute_batches = minute_batches
    env.runner.current_minute = 0
    env.runner.total_duration = total_duration

    # Enable logging
    setup_logging("INFO", None)

    # Log information about minute batches and total duration
    logging.info(f"Loaded {len(minute_batches)} minute batches.")
    logging.info(f"Total shadow run duration will be {total_duration} seconds ({total_duration/60:.2f} minutes).")

    # Start the test
    env.runner.start(1, spawn_rate=1)

    # Setup logging and stats
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    # Run the test until interrupted
    try:
        env.runner.greenlet.join()
    except KeyboardInterrupt:
        print("Stopping the test")
    finally:
        env.runner.quit()

if __name__ == "__main__":
    main()
