import logging
import time
import os
import psutil


def setup_timing():
    """Start timing and get current process for memory tracking."""
    start_time = time.monotonic()
    process = psutil.Process(os.getpid())
    return start_time, process


def log_memory(process):
    """Log current memory usage in MB."""
    mem_usage = process.memory_info().rss / 1024 / 1024
    logging.debug(f"Memory usage: {mem_usage:.2f} MB")


def finish_timing(start_time, label="operation"):
    """Log elapsed time for an operation."""
    elapsed_time = time.monotonic() - start_time
    logging.info("Finished %s. Elapsed time %.3f", label, elapsed_time)
    return elapsed_time


def log_progress(i, num, progress_counter, progress_interval=1, label="Processed"):
    """Log progress as a percentage. Returns updated progress_counter."""
    if i + 1 >= progress_counter + progress_interval or i + 1 == num:
        progress_counter = i + 1
        progress_percent = progress_counter / num * 100
        logging.info(
            f"{label} {progress_counter} of {num} ({progress_percent:.1f}%)"
        )
    return progress_counter


def get_output_path(pdf_path, suffix=""):
    """Generate an output path based on the input file name."""
    base, ext = os.path.splitext(os.path.basename(pdf_path))
    return f"{base}{suffix}.pdf"
