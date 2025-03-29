import logging
import os
from datetime import datetime
import sys
import subprocess
import argparse
from homebak.config import load_config, get_config_path
from homebak.core import backup_home_directory

def setup_logging(timestamp):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_filename = f"backup_{timestamp}.log"
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

def main():
    parser = argparse.ArgumentParser(description="homebak: backup your home directory")
    parser.add_argument("command", nargs="?", default="backup", choices=["backup", "edit-config"])
    args = parser.parse_args()

    if args.command == "edit-config":
        config_path = get_config_path()
        subprocess.run([os.getenv("EDITOR", "nano"), str(config_path)])
        return

    config = load_config()

    print("📦 Homebak is about to run with the following settings:\n")
    print(f"🔹 Backup location : {config['backup_location'].replace('$USER', os.getenv('USER'))}")
    print(f"🔹 Excluded dirs   : {', '.join(config.get('exclude_directories', [])) or 'None'}")
    print(f"🔹 Timeout (sec)   : {config.get('copy_timeout', 30)}\n")

    confirm = input("❓ Proceed with backup? [y/N]: ").strip().lower()
    if confirm != "y":
        print("❌ Backup cancelled.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    setup_logging(timestamp)
    backup_home_directory(config, timestamp)
    sys.exit(0)

