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
    parser.add_argument(
         "--debug",
         action="store_true",
         help="Enable debug mode"
    )
    parser.add_argument(
        "--s3-endpoint",
        help="Override S3 endpoint (e.g., for Minio)"
    )
    parser.add_argument(
        "--s3-profile",
        help="AWS/Minio profile to use for S3 access"
    )
    return parser.parse_args()

def main():
    args = parse_arguments()
    config_path = args.config

    if args.debug:
        import debugpy
        import os
        os.environ['GEVENT_SUPPORT'] = 'True'
        debugpy.listen(("0.0.0.0", 5678))
        print("Waiting for debugger to attach...")
        debugpy.wait_for_client()

    try:
        warmup_config = WarmupConfig.from_yaml(config_path)
        if args.s3_endpoint:
             warmup_config.s3_endpoint_override = args.s3_endpoint
             warmup_config.s3_profile = args.s3_profile
        run_warmup(warmup_config)
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()