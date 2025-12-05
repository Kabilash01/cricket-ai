import yaml
from pathlib import Path

def load_config(config_path):
    """Load YAML configuration file."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent

def get_config_path(config_name):
    """Get the full path to a config file."""
    return get_project_root() / 'configs' / config_name
