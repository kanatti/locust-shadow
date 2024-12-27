import argparse
import logging
from locust_shadow.config import WarmupConfig
from locust_shadow.runner import run_warmup

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a warmup test using Locust Shadow")
    parser.add_argument(
        "-c", "--config",
        required=True,
        help="Path to the YAML configuration file for the warmup test"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    config_path = args.config

    try:
        warmup_config = WarmupConfig.from_yaml(config_path)
        run_warmup(warmup_config)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()