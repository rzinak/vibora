import re
import fitz
import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing


class Redactor:
    @staticmethod
    def get_sensitive_data(lines):
        EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d\.]+)"
        CPF_REG = r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"

        for line in lines:
            email_match = re.search(EMAIL_REG, line, re.IGNORECASE)
            if email_match:
                yield email_match.group(1)
                continue
            cpf_match = re.search(CPF_REG, line)
            if cpf_match:
                yield cpf_match.group(0)

    def __init__(self, path):
        self.path = path

    def redaction(self):
        logging.info(f"Started redacting file: {self.path}")
        logging.info(f"File size before redaction: {os.path.getsize(self.path)} bytes")
        start_time, process = setup_timing()

        doc = fitz.open(self.path)
        redaction_counter = 0

        for page in doc:
            page.wrap_contents()
            sensitive = self.get_sensitive_data(page.get_text("text").split("\n"))
            for data in sensitive:
                areas = page.search_for(data)
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]
                redaction_counter += 1
                logging.info(f"Redacting item {data}")
                log_memory(process)
            page.apply_redactions()

        output_file = "redacted.pdf"
        doc.save(output_file)
        logging.info(f"File size after redaction: {os.path.getsize(output_file)} bytes")
        finish_timing(start_time, "redacting file")
        logging.info(f"Total sensitive items redacted: {redaction_counter}")
