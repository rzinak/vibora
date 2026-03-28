import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing


def compare_file(file1, file2):
    import fitz

    try:
        logging.info(f"Starting to compare {file1} and {file2}")
        start_time, process = setup_timing()
        with fitz.open(file1) as doc1, fitz.open(file2) as doc2:
            logging.info("Comparing number of pages...\n")
            if len(doc1) != len(doc2):
                logging.debug("Length of files do not match!")
                print("Length of files do not match!")
                return False
            else:
                logging.debug("Matching length of files!")
                logging.info("Length of files are the same!")

            logging.debug("Comparing metadata of files...\n")
            metadata1 = set(doc1.metadata.items())
            metadata2 = set(doc2.metadata.items())
            if metadata1 != metadata2:
                logging.debug("Metadata of files do not match!")
                logging.info("Metadata do not match!")
                return False
            else:
                logging.debug("Metadata is the same!")
                logging.info("Metadata is the same!")

            logging.debug("Comparing content of each page...\n")
            for i, (page1, page2) in enumerate(zip(doc1, doc2)):
                if page1.get_text() != page2.get_text():
                    logging.debug(f"Content of page {i+1} do not match!")
                    print(f"Content of page {i+1} do not match!")
                    return False
                else:
                    logging.debug(f"Content of page {i+1} matches!")
                    logging.info(f"Content of page {i+1} matches!")

                log_memory(process)

        finish_timing(start_time, "comparing files")
    except Exception as e:
        logging.exception(e)
        return False
    print("Everything matches, files are the same!")
    return True
