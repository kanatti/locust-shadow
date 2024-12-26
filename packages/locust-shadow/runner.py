from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
import logging
from warmup_user import WarmupUser
from user import DynamicMinuteBatchUser

def setup_locust_environment(config, is_warmup=False):
    if is_warmup:
        user_classes = [WarmupUser]
        env = Environment(user_classes=user_classes, host=config.host)
        env.create_local_runner()
        env.runner.warmup_config = config
    else:
        user_classes = [DynamicMinuteBatchUser]
        env = Environment(user_classes=user_classes, host=config.get_host())
        env.create_local_runner()
        minute_batches = config.get_minute_batches()
        total_duration = len(minute_batches) * 60
        env.runner.minute_batches = minute_batches
        env.runner.current_minute = 0
        env.runner.total_duration = total_duration

    setup_logging("INFO", None)
    return env

def run_locust(env: Environment, is_warmup=False):
    user_count = 1  # Always use 1 user

    env.runner.start(user_count, spawn_rate=user_count)
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    try:
        env.runner.greenlet.join()
    except KeyboardInterrupt:
        print("Stopping the test")
    finally:
        env.runner.quit()

def run_warmup(warmup_config):
    env = setup_locust_environment(warmup_config, is_warmup=True)
    logging.info(f"Starting warmup from {warmup_config.start_rps} to {warmup_config.end_rps} RPS")
    run_locust(env, is_warmup=True)

def run_shadow(shadow_config):
    env = setup_locust_environment(shadow_config)
    minute_batches = shadow_config.get_minute_batches()
    total_duration = len(minute_batches) * 60
    logging.info(f"Loaded {len(minute_batches)} minute batches.")
    logging.info(f"Total shadow run duration will be {total_duration} seconds ({total_duration/60:.2f} minutes).")
    run_locust(env)