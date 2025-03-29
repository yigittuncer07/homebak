import yaml
import shutil
from pathlib import Path
from platformdirs import user_config_dir
import importlib.resources

APP_NAME = "homebak"

def get_config_path():
    return Path(user_config_dir(APP_NAME)) / "config.yaml"

def load_config():
    config_path = get_config_path()

    if not config_path.exists():
        # First-time setup: copy bundled default config
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with importlib.resources.path("homebak", "default_config.yaml") as default:
            shutil.copy(default, config_path)
        print(f"Default config created at {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)