import argparse
import logging

from locust_shadow.config import ShadowConfig, WarmupConfig
from locust_shadow.runner import run_warmup, run_shadow

logging.basicConfig(level=logging.DEBUG)

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


def main():
    args = parse_arguments()

    if args.command == "warmup":
        print(f"Running warmup with config file: {args.config}")
        run_warmup(WarmupConfig.from_yaml(args.config))
    elif args.command == "shadow":
        print(f"Running shadow with config file: {args.config}")
        run_shadow(ShadowConfig.from_yaml(args.config))
    else:
        print("Please specify a command: warmup or shadow")

if __name__ == "__main__":
    main()
