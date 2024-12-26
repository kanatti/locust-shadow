from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
import logging
from warmup import WarmupShape, WarmupUser
from shadow import ShadowShape, ShadowUser

def _setup_locust_environment(config, is_warmup=False):
    if is_warmup:
        user_classes = [WarmupUser]
        shape = WarmupShape()
        shape.set_warmup_config(config)
        env = Environment(user_classes=user_classes, shape_class=shape, host=config.host)
        env.create_local_runner()
        env.runner.warmup_config = config
    else:
        user_classes = [ShadowUser]
        shape = ShadowShape()
        shape.set_shadow_config(config)
        env = Environment(user_classes=user_classes, shape_class=shape, host=config.get_host())
        env.create_local_runner()

    setup_logging("INFO", None)
    return env

def _run_locust(env: Environment):
    env.runner.start_shape()
    gevent.spawn(stats_printer(env.stats))
    gevent.spawn(stats_history, env.runner)

    try:
        env.runner.greenlet.join()
    except KeyboardInterrupt:
        print("Stopping the test")
    finally:
        env.runner.quit()

def run_warmup(warmup_config):
    env = _setup_locust_environment(warmup_config, is_warmup=True)
    logging.info(f"Starting warmup from {warmup_config.start_rps} to {warmup_config.end_rps} RPS")
    logging.info(f"Step duration: {warmup_config.step_duration} seconds")
    logging.info(f"RPS increment: {warmup_config.rps_increment}")
    _run_locust(env)

def run_shadow(shadow_config):
    env = _setup_locust_environment(shadow_config)
    minute_batches = shadow_config.get_minute_batches()
    total_duration = len(minute_batches) * 60
    logging.info(f"Loaded {len(minute_batches)} minute batches.")
    logging.info(f"Total shadow run duration will be {total_duration} seconds ({total_duration/60:.2f} minutes).")
    _run_locust(env)
