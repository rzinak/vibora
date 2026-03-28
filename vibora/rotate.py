import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def rotate_pdf(pdf_path, progress_interval=1):
    from PyPDF2 import PdfWriter, PdfReader

    try:
        logging.info(f"Rotating file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        num = len(reader.pages)
        progress_counter = 0
        for i, page in enumerate(reader.pages):
            logging.debug(f"Rotating page {i+1}")
            page.rotate(90)
            writer.add_page(page)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Rotated")
        output_file = "file.pdf"
        with open(output_file, "wb") as pdf_out:
            writer.write(pdf_out)
        logging.info(f"File size after rotation: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "rotating file")
    except Exception as e:
        logging.exception(e)
