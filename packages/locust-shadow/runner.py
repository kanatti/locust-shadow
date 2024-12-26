from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
import logging

def setup_locust_environment(config, user_classes):
    env = Environment(user_classes=user_classes, host=config.get_host())
    env.create_local_runner()

    minute_batches = config.get_minute_batches()
    total_duration = len(minute_batches) * 60

    # Add minute_batches and total_duration to the runner
    env.runner.minute_batches = minute_batches
    env.runner.current_minute = 0
    env.runner.total_duration = total_duration

    # Enable logging
    setup_logging("INFO", None)

    # Log information about minute batches and total duration
    logging.info(f"Loaded {len(minute_batches)} minute batches.")
    logging.info(f"Total shadow run duration will be {total_duration} seconds ({total_duration/60:.2f} minutes).")

    return env

def run_locust(env: Environment):
    env.runner.start(1, spawn_rate=1)
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    try:
        env.runner.greenlet.join()
    except KeyboardInterrupt:
        print("Stopping the test")
    finally:
        env.runner.quit()
