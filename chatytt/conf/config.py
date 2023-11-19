from pathlib import Path

import yaml


def config_path():
    return Path(__file__).parent.resolve()


def load_config():
    with open(f"{config_path()}/config.yaml", "r") as file:
        config = yaml.safe_load(file)

    return config
