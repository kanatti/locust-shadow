import yaml
import re
from dataclasses import dataclass
from typing import List, Dict, Optional

class InvalidConfigError(Exception):
    pass

@dataclass
class WarmupConfig:
    host: str
    start_rps: int
    end_rps: int
    rps_increment: int
    step_duration: int
    request_files: List[str]
    s3_endpoint_override: Optional[str] = None
    s3_profile: Optional[str] = None

    @classmethod
    def from_yaml(cls, config_path: str) -> 'WarmupConfig':
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
        config = cls(**config_data)
        config.validate_request_files()
        return config

    @staticmethod
    def is_s3_uri(path: str) -> bool:
        return path.startswith('s3://')

    @staticmethod
    def parse_s3_uri(uri: str) -> tuple:
        match = re.match(r's3://([^/]+)/(.+)', uri)
        if match:
            return match.group(1), match.group(2)
        raise ValueError(f"Invalid S3 URI: {uri}")

    def is_s3_config(self) -> bool:
        return all(self.is_s3_uri(path) for path in self.request_files)

    def validate_request_files(self):
        import logging
        logging.info(f"Validating request files: {self.request_files}")
        if not self.request_files:
            raise InvalidConfigError("No request files specified")

        is_s3 = self.is_s3_uri(self.request_files[0])
        if not all(self.is_s3_uri(file) == is_s3 for file in self.request_files):
            raise InvalidConfigError("All request files must be either local paths or S3 URIs, not a mixture")

        if is_s3:
            for uri in self.request_files:
                try:
                    self.parse_s3_uri(uri)
                except ValueError as e:
                    raise InvalidConfigError(str(e))


@dataclass
class ShadowConfig:
    host: str
    minute_batches: List[Dict]

    @classmethod
    def from_yaml(cls, config_path: str) -> 'ShadowConfig':
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(
            host=config['host'],
            minute_batches=config['minute_batches']
        )

    def get_host(self) -> str:
        return self.host

    def get_minute_batches(self) -> List[Dict]:
        return self.minute_batches
