import os
import shutil
import logging
import tarfile
from tqdm import tqdm
from homebak.utils import should_exclude, copy_file_with_timeout

def compress_backup(backup_path, output_file):
    logging.info(f"Compressing backup to {output_file}")
    total_files = sum([len(files) for _, _, files in os.walk(backup_path)])

    with tarfile.open(output_file, "w:gz") as tar:
        with tqdm(total=total_files, desc="Compressing", unit="file") as pbar:
            for root, _, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, backup_path)
                    tar.add(file_path, arcname=arcname)
                    pbar.update(1)

    shutil.rmtree(backup_path)
    logging.info(f"Compression completed. Backup saved as {output_file}")

def backup_home_directory(config, timestamp, dry_run=False):
    home_dir = os.path.expanduser("~")
    backup_dir = os.path.expanduser(config["backup_location"]).replace("$USER", os.getenv('USER'))
    excluded_directories_names = config.get("exclude_directory_names", [])
    print(excluded_directories_names)
    copy_timeout = config.get("copy_timeout", 30)

    failed_files = []

    if not os.path.exists(backup_dir):
        if not dry_run: os.makedirs(backup_dir)
        logging.info(f"Created backup directory: {backup_dir}")

    backup_path = os.path.join(backup_dir, f"backup_{timestamp}")
    logging.info(f"Starting backup: {backup_path}")
    if not dry_run: os.makedirs(backup_path)
    

    for root, dirs, files in os.walk(home_dir):
        
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), excluded_directories_names)]

        excluded_dirs = [d for d in dirs if should_exclude(os.path.join(root, d), excluded_directories_names)]

        for d in excluded_dirs:
            logging.info(f"Skipping excluded directory: {os.path.join(root, d)}")

        rel_path = os.path.relpath(root, home_dir)
        dest_path = os.path.join(backup_path, rel_path)
        if not dry_run: os.makedirs(dest_path, exist_ok=True)

        with tqdm(total=len(files), desc=f"Copying {rel_path}" if not dry_run else f"[Dry Run] Copying {rel_path}", unit="file") as pbar:
            for file in files:
                file_src_path = os.path.join(root, file)
                file_dest_path = os.path.join(dest_path, file)
                
                # exclude symbolic links
                if os.path.islink(file_src_path):
                    logging.info(f"Skipping symbolic link: {file_src_path}")
                    pbar.update(1)
                    continue
                
                if not dry_run:
                    if not copy_file_with_timeout(file_src_path, file_dest_path, copy_timeout):
                        logging.error(f"Failed to copy {file_src_path} within {copy_timeout} seconds.")
                        failed_files.append(file_src_path)
                    else:
                        logging.info(f"Copied: {file_src_path}")
                    pbar.update(1)
                else:
                    logging.info(f"[Dry Run] Would copy: {file_src_path}")


    logging.info(f"Backup completed successfully: {backup_path}")
    if dry_run:
        print("🟡 Dry run complete.")
        print(f"🗂 Backup would be created at: {backup_path}.tar.gz")
        print("📁 No files were copied.")
        return


    compressed_file = os.path.join(backup_dir, f"backup_{timestamp}.tar.gz")
    compress_backup(backup_path, compressed_file)

    if failed_files:
        logging.info("The following files failed to copy:")
        for failed_file in sorted(failed_files):
            logging.info(failed_file)

    else:
        logging.info("All files copied successfully.")

    logging.info("Backup process completed.")