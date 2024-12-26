from dataclasses import dataclass
import yaml
from typing import List, Dict

@dataclass
class WarmupConfig:
    host: str
    start_rps: int
    rps_increment: int
    step_duration: int
    end_rps: int
    request_files: List[str]

    @classmethod
    def from_yaml(cls, config_path: str) -> 'WarmupConfig':
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return cls(**config)

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
