import threading
from collections import deque
import logging
import math
from contextlib import contextmanager
import time

from locust import LoadTestShape, HttpUser, constant_pacing

class StrictRpsShape(LoadTestShape):
    """
    A custom LoadTestShape that maintains a strict RPS (Requests Per Second) rate
    by dynamically adjusting the number of users and their wait times.

    This shape class monitors request latencies and adjusts the user count to
    maintain the desired RPS, even as system performance changes.
    """
    abstract = True

    def __init__(self):
        super().__init__()
        self.latency_buffer = deque(maxlen=100) # Store last 100 latencies
        self.latency_lock = threading.Lock() # Add a lock for thread-safety
        self.current_user_count = 1
        self.slab_size_percent = 0.3 # 10% of current user count
        self.buffer_rate = 0.2 # 20% increase when ramping up
        self.last_rps = None
        self.last_user_count = None

    def record_request_latency(self, latency):
        """
        Record a new request latency in the latency buffer.

        Args:
            latency (float): The latency of a request in seconds.
        """
        self.latency_buffer.append(latency)

    def update_for_rps(self, current_rps):
        """
        Update the users and wait_time to maintain current_rps
        """
        avg_latency = self._get_current_average_latency()
        self.current_user_count = self._calculate_user_count(current_rps, avg_latency)
        self._update_user_wait_time(current_rps)
        return (self.current_user_count, avg_latency)

    def _get_current_average_latency(self):
        """
        Calculate and return the current average latency from the latency buffer.
        """
        if not self.latency_buffer:
            return 1.0
        with self.latency_lock:
            return sum(self.latency_buffer) / len(self.latency_buffer)


    def _calculate_user_count(self, current_rps, avg_latency):
        """
        Calculate the number of users needed to maintain the current RPS given the average latency.
        """
        raw_count = current_rps * avg_latency
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

    def _update_user_wait_time(self, current_rps):
        """
        Update the wait time for all user classes based on the current RPS and user count.
        """
        if current_rps != self.last_rps or self.current_user_count != self.last_user_count:
            for user in self.runner.user_classes:
                if hasattr(user, 'update_wait_time'):
                    user.update_wait_time(current_rps, self.current_user_count)

            self.last_rps = current_rps
            self.last_user_count = self.current_user_count



class StrictRpsUser(HttpUser):
    """
    A custom HttpUser class designed to work with StrictRpsShape.
    
    This class provides methods for measuring request latency and updating
    wait times to maintain a strict RPS (Requests Per Second) rate.
    """

    wait_time = constant_pacing(1)  # Default value, will be updated

    def __init__(self, environment):
        super().__init__(environment)

    @contextmanager
    def measure_latency(self):
        """
        A context manager for measuring the latency of a request.

        Usage:
            with self.measure_latency():
                self.client.get("/")

        This will automatically record the latency of the request.
        """
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            latency = end_time - start_time
            self._record_latency(latency)

    def _record_latency(self, latency):
        """
        Record the latency of a request to the StrictRpsShape.

        Args:
            latency (float): The latency of the request in seconds.
        """
        if isinstance(self.environment.shape_class, StrictRpsShape):
            self.environment.shape_class.record_request_latency(latency)

    @classmethod
    def update_wait_time(cls, current_rps, user_count):
        """
        Update the wait time for all users of this class based on the current RPS and user count.

        Args:
            current_rps (float): The current target requests per second.
            user_count (int): The current number of users.
        """
        if user_count > 0:
            pacing_per_user = user_count / current_rps
            cls.wait_time = constant_pacing(pacing_per_user)
        else:
            cls.wait_time = constant_pacing(1)

        logging.info(f"Updated wait time: RPS={current_rps}, Users={user_count}, "
                    f"Pacing={pacing_per_user:.4f}s")
