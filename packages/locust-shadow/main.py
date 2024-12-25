import json
import argparse
from locust import HttpUser, task, between
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent

class MinuteBatchUser(HttpUser):
    wait_time = between(0.1, 1)  # Time between requests

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = []
        self.request_index = 0

    def on_start(self):
        # Load requests from the JSONL file
        with open("dev/test_minute_batch/requests1.jsonl", "r") as f:
            self.requests = [json.loads(line) for line in f]

    @task
    def execute_request(self):
        if self.request_index < len(self.requests):
            request = self.requests[self.request_index]
            self.client.get(request["path"], params=request["params"])
            self.request_index += 1
        else:
            # Stop the user when all requests are executed
            self.environment.runner.quit()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Locust Shadow Runner")
    parser.add_argument('--host', type=str, default="http://localhost:8000",
                        help='Host to test (default: http://localhost:8000)')
    args = parser.parse_args()

    # Set up the Locust environment
    env = Environment(user_classes=[MinuteBatchUser], host=args.host)
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
