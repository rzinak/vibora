import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def encrypt_pdf(pdf_path, password, progress_interval=1):
    from PyPDF2 import PdfReader, PdfWriter

    try:
        logging.info(f"Started encrypting PDF file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()
        out = PdfWriter()
        reader = PdfReader(pdf_path)
        num = len(reader.pages)
        progress_counter = 0
        for i in range(num):
            logging.debug(f"Encrypting page {i+1}")
            out.add_page(reader.pages[i])
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Encrypted")
        out.encrypt(password)
        output_file = "file.pdf"
        with open(output_file, "wb") as f:
            out.write(f)
        logging.info(f"File size after encryption: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "encrypting file")
    except Exception as e:
        logging.exception(e)
