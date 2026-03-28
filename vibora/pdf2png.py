import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def pdf_to_png(pdf_path, progress_interval=1):
    from pdf2image import convert_from_path

    try:
        logging.info(f"Converting PDF file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        logging.info("Files that have more than one page will be converted into multiple images.")
        start_time, process = setup_timing()
        images = convert_from_path(pdf_path)
        num = len(images)
        progress_counter = 0
        for i in range(num):
            logging.debug(f"Converting page {i+1}")
            output_file = f"page{i}.png"
            images[i].save(output_file)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Converted")
        finish_timing(start_time, "converting file")
    except Exception as e:
        logging.exception(e)
