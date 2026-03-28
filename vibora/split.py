import os
import logging
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def split_pdf(pdf_path, progress_interval=1):
    from PyPDF2 import PdfReader, PdfWriter

    try:
        logging.info(f"Started splitting PDF file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()
        fname = os.path.splitext(os.path.basename(pdf_path))[0]
        pdf = PdfReader(pdf_path)
        num = len(pdf.pages)
        if num == 1:
            print("File has 1 page, can't split it.")
            return
        progress_counter = 0
        for i in range(num):
            logging.debug(f"Splitting page {i+1}")
            pdf_writer = PdfWriter()
            pdf_writer.add_page(pdf.pages[i])
            output_filename = f"{fname}_page_{i + 1}.pdf"
            with open(output_filename, "wb") as out:
                pdf_writer.write(out)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Split")
        finish_timing(start_time, "splitting files")
    except Exception as e:
        logging.exception(e)
