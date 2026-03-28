import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def watermark_pdf(pdf_path, watermark, progress_interval=1):
    from PyPDF2 import PdfReader, PdfWriter

    try:
        logging.info(f"Adding watermark to file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        logging.info(f"Watermark file size: {os.path.getsize(watermark)} bytes")
        start_time, process = setup_timing()
        watermark_instance = PdfReader(watermark)
        watermark_page = watermark_instance.pages[0]
        pdf_reader = PdfReader(pdf_path)
        pdf_writer = PdfWriter()
        num = len(pdf_reader.pages)
        progress_counter = 0
        for i in range(num):
            logging.debug(f"Adding watermark to page {i+1}")
            page = pdf_reader.pages[i]
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Watermarked")
        output_file = "watermarked.pdf"
        with open(output_file, "wb") as out:
            pdf_writer.write(out)
        logging.info(f"File size after adding watermark: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "adding watermark to file")
    except Exception as e:
        logging.exception(e)
