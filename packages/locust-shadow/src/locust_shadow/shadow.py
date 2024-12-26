from locust import LoadTestShape, HttpUser, task, constant_throughput
import logging
from queue import Queue
import json
import gevent
import threading

from locust_shadow.strict_rps import StrictRpsShape, StrictRpsUser

class ShadowShape(StrictRpsShape):
    refill_lock = threading.Lock()

    def __init__(self):
        super().__init__()
        self.shadow_config = None
        self.minute_batches = []
        self.current_minute = None
        self.request_queue = Queue()
        self.original_requests = []
        self.total_duration = 0
        self.shadow_complete = False

    def tick(self):
        run_time = self.get_run_time()
        if self.shadow_config is None:
            logging.warning("Shadow config is not set. Stopping.")
            return None

        if run_time >= self.total_duration and not self.shadow_complete:
            logging.info("Shadow test complete. Stopping.")
            self.shadow_complete = True
            self.stop_runner()
            return None
        
        if self.shadow_complete:
            return None

        current_minute = int(run_time / 60)
        
        # Initialize for the first tick or update when the minute changes
        if self.current_minute is None or current_minute != self.current_minute:
            self.update_minute_batch(current_minute)

        current_batch = self.minute_batches[self.current_minute]
        current_rps = current_batch.get("rps", 1)

        user_count, avg_latency = self.update_for_rps(current_rps)

        logging.info(f"Minute: {current_minute}, Target RPS: {current_rps}, "
                     f"Avg Latency: {avg_latency:.2f}s, Users: {user_count}")

        return (user_count, user_count)  # (user_count, spawn_rate)

    def set_shadow_config(self, config):
        self.shadow_config = config
        self.minute_batches = config.get_minute_batches()
        self.total_duration = len(self.minute_batches) * 60

    def update_minute_batch(self, new_minute):
        self.current_minute = new_minute % len(self.minute_batches)
        current_batch = self.minute_batches[self.current_minute]
        
        # Clear the existing queue and original requests
        while not self.request_queue.empty():
            self.request_queue.get()
        self.original_requests.clear()

        # Load new requests into the queue and store original requests
        for request_file in current_batch.get("request_files", []):
            with open(request_file, "r") as f:
                for line in f:
                    request = json.loads(line)
                    self.request_queue.put(request)
                    self.original_requests.append(request)

        logging.info(f"Updated to minute batch {self.current_minute}")

    def get_next_request(self):
        if self.request_queue.empty():
            with self.refill_lock:  # Only lock the refill operation
                if self.request_queue.empty():  # Double-check after acquiring the lock
                    # Refill the queue with the original requests
                    for request in self.original_requests:
                        self.request_queue.put(request)
                    logging.info(f"Refilled request queue for minute {self.current_minute}")

        return self.request_queue.get(block=False) if not self.request_queue.empty() else None

    def stop_runner(self):
        if self.runner is not None:
            self.runner.quit()

class ShadowUser(StrictRpsUser):
    def __init__(self, environment):
        super().__init__(environment)
        self.shape = None

    def on_start(self):
        self.shape = self.environment.shape_class

    @task
    def execute_request(self):
        request = self.shape.get_next_request()
        if request:
            with self.measure_latency():
                self.client.get(request["path"], params=request["params"])
        else:
            gevent.sleep(0.1)  # Small sleep to prevent busy-waiting
