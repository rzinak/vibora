import os
import logging
from vibora.utils import setup_timing, log_memory, finish_timing


def rename_file(file, new_name):
    try:
        logging.info(f"Renaming file {file}")
        logging.info(f"File size: {os.path.getsize(file)} bytes")
        start_time, process = setup_timing()
        os.rename(file, new_name)
        log_memory(process)
        logging.info(f"File size after changing name: {os.path.getsize(new_name)} bytes")
        finish_timing(start_time, "renaming file")
    except Exception as e:
        logging.exception(e)
