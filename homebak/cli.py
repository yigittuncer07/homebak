from homebak import __version__
import logging
import os
from datetime import datetime
import sys
import subprocess
import argparse
from homebak.config import load_config, get_config_path
from homebak.core import backup_home_directory
from platformdirs import user_state_dir
from pathlib import Path

def setup_logging(timestamp):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    log_dir = Path(user_state_dir("homebak")) / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / f"backup_{timestamp}.log"

    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return f"📄 Log file: {log_path}"


def main():
    parser = argparse.ArgumentParser(description="homebak: backup your home directory")
    parser.add_argument("command", nargs="?", default="backup", choices=["backup", "edit-config"])
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be backed up, but don’t do it")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if args.command == "edit-config":
        config_path = get_config_path()
        subprocess.run([os.getenv("EDITOR", "nano"), str(config_path)])
        return

    config = load_config()

    mode = "🟡 Dry Run" if args.dry_run else "🟢 Real Backup"
    print(f"\n📦 Homebak is about to run — {mode} mode:\n")
    print(f"🔹 Backup location : {config['backup_location'].replace('$USER', os.getenv('USER'))}")
    print(f"🔹 Excluded directory names   : {', '.join(config.get('exclude_directory_names', [])) or 'None'}")
    print(f"🔹 Timeout (sec)   : {config.get('copy_timeout', 30)}")
    print(f"🕓 Timestamp       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if not args.yes:
        confirm = input("❓ Proceed? [y/N]: ").strip().lower()
        if confirm != "y":
            print("❌ Backup cancelled.")
            return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path_message = setup_logging(timestamp)
    backup_home_directory(config, timestamp, dry_run=args.dry_run)
    print(log_path_message)
    sys.exit(0)

