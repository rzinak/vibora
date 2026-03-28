import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def decrypt_pdf(pdf_path, password, progress_interval=1):
    from PyPDF2 import PdfReader, PdfWriter

    try:
        out = PdfWriter()
        reader = PdfReader(pdf_path)
        if not reader.is_encrypted:
            print("File is not encrypted")
            return
        try:
            logging.info(f"Started decrypting PDF file: {pdf_path}")
            logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
            start_time, process = setup_timing()
            reader.decrypt(password)
            num = len(reader.pages)
            progress_counter = 0
            for i in range(num):
                logging.debug(f"Decrypting page {i+1}")
                out.add_page(reader.pages[i])
                log_memory(process)
                progress_counter = log_progress(i, num, progress_counter, progress_interval, "Decrypted")
            output_file = "file_decrypted.pdf"
            with open(output_file, "wb") as f:
                out.write(f)
            logging.info(f"File size after decryption: {os.path.getsize(output_file)} bytes")
            finish_timing(start_time, "decrypting file")
        except Exception:
            print("An error occurred. Is the password correct?")
    except Exception as e:
        logging.exception(e)
