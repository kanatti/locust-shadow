import random
import json
import logging
import time
import threading
import math
from collections import deque

from locust import LoadTestShape, HttpUser, task, constant_pacing

class WarmupShape(LoadTestShape):
    def __init__(self):
        super().__init__()
        self.warmup_config = None
        self.expected_steps = None
        self.warmup_complete = False
        self.latency_buffer = deque(maxlen=100)  # Store last 100 latencies
        self.latency_lock = threading.Lock()  # Add a lock for thread-safety
        self.current_user_count = 1
        self.slab_size_percent = 0.3  # 10% of current user count
        self.buffer_rate = 0.2  # 20% increase when ramping up
        self.last_rps = None
        self.last_user_count = None

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

        avg_latency = self.get_current_average_latency()
        self.current_user_count = self.calculate_user_count(current_rps, avg_latency)

        logging.info(f"Step: {current_step}/{self.expected_steps}, Target RPS: {current_rps}, "
                     f"Avg Latency: {avg_latency:.2f}s, Users: {self.current_user_count}")

        # Update wait time if RPS or user count has changed
        if current_rps != self.last_rps or self.current_user_count != self.last_user_count:
            for user in self.runner.user_classes:
                if hasattr(user, 'update_wait_time'):
                    user.update_wait_time(current_rps, self.current_user_count)

            # Update last known values
            self.last_rps = current_rps
            self.last_user_count = self.current_user_count

        return (self.current_user_count, self.current_user_count)

    def get_current_average_latency(self):
        with self.latency_lock:
            if not self.latency_buffer:
                return 1.0  # Default to 1 second if no data
            return sum(self.latency_buffer) / len(self.latency_buffer)

    def record_request_latency(self, latency):
        self.latency_buffer.append(latency) # Dequeue append is thread-safe.

    def calculate_user_count(self, current_rps, avg_latency):
        # Calculate raw user count based on current RPS and average latency
        raw_count = current_rps * avg_latency

        # Add some extra buffer
        new_user_count = raw_count * (1 + self.buffer_rate)

        # Apply slab so that we dont make small deltas often.
        slab_size = max(int(self.current_user_count * self.slab_size_percent), 1)
        slabbed_user_count = math.ceil(new_user_count / slab_size) * slab_size

        # If the new count is higher, allow it to increase
        if slabbed_user_count > self.current_user_count:
            return slabbed_user_count

        # If the new count is lower, only decrease it slowly, to avoid thrashing.
        # We make it slow by only allowing a decrease every 1 minute (60 seconds)
        if slabbed_user_count < self.current_user_count:
            if self.get_run_time() % 60 == 0:
                return slabbed_user_count

        return self.current_user_count

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
    wait_time = constant_pacing(1)  # Default value, will be updated

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
        start_time = time.time()
        response = self.client.get(request["path"], params=request["params"])
        end_time = time.time()

        latency = end_time - start_time
        if isinstance(self.environment.shape_class, WarmupShape):
            self.environment.shape_class.record_request_latency(latency)

    @classmethod
    def update_wait_time(cls, current_rps, user_count):
        if user_count > 0:
            # Calculate the required pacing per user
            pacing_per_user = user_count / current_rps
            cls.wait_time = constant_pacing(pacing_per_user)
        else:
            cls.wait_time = constant_pacing(1)  # Default to 1 second pacing if user_count is 0
        
        logging.info(f"Updated wait time: RPS={current_rps}, Users={user_count}, "
                      f"Pacing={pacing_per_user:.4f}s")
