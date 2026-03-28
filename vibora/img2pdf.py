import img2pdf
import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing


def image_to_pdf(img_path):
    try:
        logging.info(f"Converting file '{img_path}' to PDF")
        logging.info(f"File size: {os.path.getsize(img_path)} bytes")
        start_time, process = setup_timing()
        pdf_bytes = img2pdf.convert(img_path)
        output_file = "file.pdf"
        with open(output_file, "wb") as f:
            f.write(pdf_bytes)
        log_memory(process)
        logging.info(f"PDF file size: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "converting image to PDF")
    except Exception as e:
        logging.exception(e)
