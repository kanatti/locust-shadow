from locust import LoadTestShape
import logging

class WarmupShape(LoadTestShape):
    def __init__(self):
        super().__init__()
        self.warmup_config = None
        self.expected_steps = None
        self.warmup_complete = False

    def tick(self):
        run_time = self.get_run_time()
        if self.warmup_config is None:
            logging.warning("Warmup config is not set. Stopping the test.")
            return None

        if self.expected_steps is None:
            self.expected_steps = self.calculate_expected_steps()

        current_step = int(run_time / self.warmup_config.step_duration)

        if current_step > self.expected_steps and not self.warmup_complete:
            logging.info("Warmup complete. Stopping the test.")
            self.warmup_complete = True
            self.stop_runner()
            return None

        if self.warmup_complete:
            return None

        current_rps = min(
            self.warmup_config.start_rps + current_step * self.warmup_config.rps_increment,
            self.warmup_config.end_rps
        )

        # Estimate the number of users needed to achieve the desired RPS
        user_count = int(current_rps * 1.2)  # Add 20% more users to account for wait times

        logging.info(f"Current step: {current_step}/{self.expected_steps}, Target RPS: {current_rps}, User count: {user_count}")

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