import codecs
import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing


def txt_to_pdf(txt_path):
    from fpdf import FPDF

    try:
        logging.info(f"Started converting file: {txt_path}")
        logging.info(f"TXT file size: {os.path.getsize(txt_path)} bytes")
        start_time, process = setup_timing()
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        with codecs.open(txt_path, "r", encoding="utf-8") as f:
            logging.debug(f"Converting file {txt_path} to .PDF")
            for line in f:
                encoded_line = line.encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 10, txt=encoded_line, align="J")
                log_memory(process)
        output_file = "myfile.pdf"
        pdf.output(output_file)
        logging.info(f"PDF file size: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "converting file")
    except Exception as e:
        logging.exception(e)
