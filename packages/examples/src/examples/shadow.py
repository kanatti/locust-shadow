import argparse
import logging
from locust_shadow.config import ShadowConfig
from locust_shadow.runner import run_shadow

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run a shadow test using Locust Shadow")
    parser.add_argument(
        "-c", "--config",
        required=True,
        help="Path to the YAML configuration file for the shadow test"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    config_path = args.config

    try:
        shadow_config = ShadowConfig.from_yaml(config_path)
        run_shadow(shadow_config)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()
