import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def pdf_to_text(pdf_path, progress_interval=1):
    from PyPDF2 import PdfReader

    try:
        logging.info(f"Started converting file: {pdf_path}")
        logging.info(f"Size of file {pdf_path}: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()
        reader = PdfReader(pdf_path)
        num = len(reader.pages)
        progress_counter = 0
        with open("file.txt", "w", encoding="utf-8") as f:
            for i, page in enumerate(reader.pages):
                logging.debug(f"Converting page {i+1}")
                text = page.extract_text()
                if text:
                    f.write(text)
                log_memory(process)
                progress_counter = log_progress(i, num, progress_counter, progress_interval, "Converted")
        logging.info(f"Size of file.txt: {os.path.getsize('file.txt')} bytes")
        finish_timing(start_time, "converting file")
    except Exception as e:
        logging.exception(e)
