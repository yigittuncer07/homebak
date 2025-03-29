# 🏠 homebak

**homebak** is a simple, configurable tool for backing up your home directory on Linux.  
Exclude what you don't need, compress the rest, and keep your data safe.

## 🚀 Features

- ⚙️ Configurable via YAML (`~/.config/homebak/config.yaml`)
- 🗃 Exclude directories by name (e.g. `.cache`, `venv`, `datasets`)
- 📦 Compressed `.tar.gz` output
- 🧪 Dry run mode (`--dry-run`)
- 🧼 Clean CLI with progress bars
- 📝 Config editing via `homebak edit-config`

## 📦 Installation

```bash
pip install homebak
```

## 📁 Example Usage

```bash
homebak               # Run with confirmation
homebak --yes         # Skip confirmation
homebak --dry-run     # Simulate backup only
homebak edit-config   # Open config file in $EDITOR
```

## ⚙️ Config Example

Located at `~/.config/homebak/config.yaml`:

```yaml
backup_location: "/media/$USER/backup/backups"
copy_timeout: 60

exclude_directory_names:
  - ".cache"
  - ".venv"
  - "datasets"
  - "snap"
```

## 🧠 Why use homebak?

Just run it. `homebak` will:
1. Walk your home directory
2. Exclude folders you don't care about
3. Copy the rest with timeout protection
4. Compress everything into a single `.tar.gz` archive