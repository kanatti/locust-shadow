import argparse
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
from config import ShadowConfig
import logging

from user import DynamicMinuteBatchUser
from runner import setup_locust_environment, run_locust

def parse_arguments():
    parser = argparse.ArgumentParser(description="Locust Shadow - Replay production traffic patterns")
    parser.add_argument("config", help="Path to the config.yaml file")
    return parser.parse_args()


def main():
    args = parse_arguments()
    config = ShadowConfig.from_yaml(args.config)

    env = setup_locust_environment(config, [DynamicMinuteBatchUser])
    run_locust(env)

if __name__ == "__main__":
    main()
