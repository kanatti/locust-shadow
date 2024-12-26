import random
import json
import logging

from locust import LoadTestShape, HttpUser, task, constant_throughput

class WarmupShape(LoadTestShape):
    def __init__(self):
        super().__init__()
        self.warmup_config = None
        self.expected_steps = None
        self.warmup_complete = False

    def tick(self):
        run_time = self.get_run_time()
        if self.warmup_config is None:
            logging.warning("Warmup config is not set. Stopping.")
            return None

        if self.expected_steps is None:
            self.expected_steps = self.calculate_expected_steps()

        current_step = int(run_time / self.warmup_config.step_duration)

        if current_step > self.expected_steps and not self.warmup_complete:
            logging.info("Warmup complete. Stopping.")
            self.warmup_complete = True
            self.stop_runner()
            return None

        if self.warmup_complete:
            return None

        current_rps = min(
            self.warmup_config.start_rps + current_step * self.warmup_config.rps_increment,
            self.warmup_config.end_rps
        )

        # Calculate the number of users needed to achieve the desired RPS
        user_count = max(1, int(current_rps))  # Ensure at least 1 user

        logging.info(f"Current step: {current_step}/{self.expected_steps}, Target RPS: {current_rps}, User count: {user_count}")

        # Update the wait time for all users
        for user in self.runner.user_classes:
            if hasattr(user, 'update_wait_time'):
                user.update_wait_time(current_rps, user_count)

        return (user_count, user_count)  # (user_count, spawn_rate)
    
    def stop_runner(self):
        if self.runner is not None:
            self.runner.quit()

    def set_warmup_config(self, config):
        self.warmup_config = config
        self.expected_steps = self.calculate_expected_steps()

    def calculate_expected_steps(self):
        if self.warmup_config is None:
            return 0
        total_rps_increase = self.warmup_config.end_rps - self.warmup_config.start_rps
        return int(total_rps_increase / self.warmup_config.rps_increment) + 1

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
