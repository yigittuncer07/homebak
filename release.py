#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

REQUIRED_PACKAGES = ["build", "twine"]

def ensure_dependencies():
    for package in REQUIRED_PACKAGES:
        try:
            __import__(package)
        except ImportError:
            print(f"📦 Installing missing package: {package}")
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)

def update_version_in_file(file_path, old, new):
    text = Path(file_path).read_text()
    text = text.replace(old, new)
    Path(file_path).write_text(text)

def main():
    if len(sys.argv) != 2:
        print("Usage: ./release.py <new-version>")
        sys.exit(1)

    ensure_dependencies()

    new_version = sys.argv[1]
    init_file = Path("homebak/__init__.py")
    pyproject_file = Path("pyproject.toml")

    init_text = init_file.read_text()
    old_version_line = [line for line in init_text.splitlines() if "__version__" in line][0]
    old_version = old_version_line.split("=")[1].strip().strip('"')

    if old_version == new_version:
        print(f"⚠️  Version {new_version} already set. Please bump it.")
        sys.exit(1)

    print(f"🔧 Bumping version: {old_version} → {new_version}")

    update_version_in_file(init_file, old_version, new_version)
    update_version_in_file(pyproject_file, old_version, new_version)

    subprocess.run(["rm", "-rf", "dist/"])
    subprocess.run([sys.executable, "-m", "build"], check=True)
    subprocess.run([sys.executable, "-m", "twine", "upload", *Path("dist").glob("*")], check=True)

if __name__ == "__main__":
    main()
