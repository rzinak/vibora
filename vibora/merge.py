import os
import logging
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def merge_pdf(*pdf_files, progress_interval=1):
    from PyPDF2 import PdfMerger

    try:
        logging.info(f"Started merging files: {pdf_files}")
        start_time, process = setup_timing()
        total_size = 0
        num = len(pdf_files)
        progress_counter = 0
        for pdf_file in pdf_files:
            file_size = os.path.getsize(pdf_file)
            total_size += file_size
            logging.info(f"Size of {pdf_file}: {file_size} bytes")
        logging.info(f"Total size of files: {total_size} bytes")
        merger = PdfMerger()
        for i, pdf_file in enumerate(pdf_files):
            logging.debug(f"Merging file {i+1}")
            with open(pdf_file, "rb") as f:
                merger.append(f)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Merged")
        output_file = "merged_file.pdf"
        merger.write(output_file)
        merger.close()
        logging.info(f"File size after merge: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "merging files")
    except Exception as e:
        logging.exception(e)


def merge_pdf_directory(directory_path, progress_interval=1):
    from PyPDF2 import PdfMerger

    try:
        logging.info(f"Started merging files in directory: {directory_path}")
        start_time, process = setup_timing()
        merger = PdfMerger()
        pdf_files = sorted(
            f for f in os.listdir(directory_path) if f.endswith(".pdf")
        )
        num = len(pdf_files)
        progress_counter = 0
        for i, pdf_file in enumerate(pdf_files):
            logging.debug(f"Merging file {i+1}")
            with open(os.path.join(directory_path, pdf_file), "rb") as f:
                merger.append(f)
            log_memory(process)
            progress_counter = log_progress(i, num, progress_counter, progress_interval, "Merged")
        output_file = "mergedall_file.pdf"
        merger.write(output_file)
        merger.close()
        logging.info(f"File size after merge: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "merging files")
    except Exception as e:
        logging.exception(e)
