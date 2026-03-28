import logging
import os
from concurrent.futures import ThreadPoolExecutor
from PyPDF2 import PdfReader, PdfWriter
from tqdm import tqdm
from typing import Optional
from vibora.utils import setup_timing, log_memory, finish_timing, log_progress


def compress_pdf(
    pdf_path,
    output: Optional[str] = None,
    progress_interval=1,
    num_threads=1,
):
    logger = logging.getLogger(__name__)

    try:
        if not os.path.isfile(pdf_path) or not pdf_path.lower().endswith(".pdf"):
            raise ValueError(
                "Invalid input file. Please provide a valid PDF file path."
            )

        logging.info(f"Started compressing PDF file: {pdf_path}")
        logging.info(f"File size before compression: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        num = len(reader.pages)
        progress_counter = 0

        def compress_page(page):
            page.compress_content_streams()
            return page

        if num_threads > 1:
            with ThreadPoolExecutor(max_workers=num_threads) as executor:
                compressed_pages = list(executor.map(compress_page, reader.pages))
        else:
            compressed_pages = [compress_page(page) for page in reader.pages]

        with tqdm(
            total=num,
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}{postfix}]",
        ) as pbar:
            for i, page in enumerate(compressed_pages):
                writer.add_page(page)
                log_memory(process)
                if i + 1 >= progress_counter + progress_interval or i + 1 == num:
                    progress_counter = i + 1
                    pbar.update(1)

        if output is None:
            output_file = "file.pdf"
        else:
            output_file = output + ".pdf"

        with open(output_file, "wb") as f:
            try:
                writer.write(f)
            except Exception as e:
                logging.exception(e)
                raise

        finish_timing(start_time, "compressing file")
        logging.info(f"File size after compression: {os.path.getsize(output_file)} bytes")
        size_variation = os.path.getsize(pdf_path) - os.path.getsize(output_file)
        percentage_variation = (size_variation / os.path.getsize(pdf_path)) * 100
        logging.info(f"File size variation: -{size_variation} bytes")
        logging.info("Percentage variation comparing to original file: -%.2f%%", percentage_variation)

    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
