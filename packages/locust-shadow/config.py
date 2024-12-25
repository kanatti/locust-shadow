import yaml
from typing import List, Dict

class Config:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        self.host: str = config['host']
        self.minute_batches: List[Dict] = config['minute_batches']

    def get_host(self) -> str:
        return self.host

    def get_minute_batches(self) -> List[Dict]:
        return self.minute_batches