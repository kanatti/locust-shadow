import argparse
from locust.env import Environment
from locust.stats import stats_printer, stats_history
from locust.log import setup_logging
import gevent
from config import ShadowConfig, WarmupConfig
import logging

from user import DynamicMinuteBatchUser
from runner import setup_locust_environment, run_locust

def parse_arguments():
    parser = argparse.ArgumentParser(description="Locust Shadow - Replay production traffic patterns and perform warmup")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Warmup command
    warmup_parser = subparsers.add_parser("warmup", help="Run warmup")
    warmup_parser.add_argument("config", help="Path to the warmup config YAML file")

    # Shadow command
    shadow_parser = subparsers.add_parser("shadow", help="Run shadow testing")
    shadow_parser.add_argument("config", help="Path to the shadow config YAML file")

    return parser.parse_args()

def run_warmup(config_path):
    print(f"Running warmup with config file: {config_path}")
    config = WarmupConfig.from_yaml(config_path)
    env = setup_locust_environment(config, True)
    run_locust(env)

def run_shadow(config_path):
    config = ShadowConfig.from_yaml(config_path)
    env = setup_locust_environment(config, False)
    run_locust(env)

def main():
    args = parse_arguments()

    if args.command == "warmup":
        run_warmup(args.config)
    elif args.command == "shadow":
        run_shadow(args.config)
    else:
        print("Please specify a command: warmup or shadow")

if __name__ == "__main__":
    main()
