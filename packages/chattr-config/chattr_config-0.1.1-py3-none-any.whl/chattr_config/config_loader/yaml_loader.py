from typing import Any, Dict

import os

import yaml


class YamlLoader:
    @staticmethod
    def load_file(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {}

        with open(file_path, "r") as f:
            config = yaml.load(f, Loader=yaml.Loader)
        return config or {}
