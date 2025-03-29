import os
import shutil
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError

def should_exclude(path, excluded_names):
    parts = path.split(os.sep)
    if not excluded_names:
        return False
    if os.path.islink(path):
        return True
    if any(part in excluded_names for part in parts):
        return True
    # print(f"parts: {parts}, excluded_names: {excluded_names}")
    return False



def copy_file_with_timeout(src, dest, timeout):
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(shutil.copy2, src, dest)
        try:
            future.result(timeout=timeout)
            return True
        except TimeoutError:
            return False
        except (shutil.SpecialFileError, OSError, IOError) as e:
            logging.error(f"Failed to copy {src}: {e}")
            return False
