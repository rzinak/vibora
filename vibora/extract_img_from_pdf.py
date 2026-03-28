import fitz
import io
import logging
import os
from vibora.utils import setup_timing, log_memory, finish_timing


def extract_img_from_pdf(pdf_path):
    try:
        logging.info(f"Extracting images from file: {pdf_path}")
        logging.info(f"File size: {os.path.getsize(pdf_path)} bytes")
        start_time, process = setup_timing()

        pdf_file = fitz.open(pdf_path)
        for page_index in range(len(pdf_file)):
            page = pdf_file[page_index]
            image_list = page.get_images()
            logging.debug(f"Extracting image from page {page_index + 1}")
            if image_list:
                print(f"Found a total of {len(image_list)} in page {page_index}")
            else:
                print("No images found")
            for image_index, img in enumerate(image_list, start=1):
                logging.debug(f"Extracting image {image_index} | Image Info: {img}")
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                log_memory(process)

                output_file = f"Image{page_index+1}_{image_index}.{image_ext}"
                with open(output_file, "wb") as f:
                    f.write(image_bytes)

        finish_timing(start_time, "extracting image(s) from file")
    except Exception as e:
        logging.exception(e)
