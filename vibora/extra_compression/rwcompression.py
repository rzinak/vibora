from pdfrw import PdfReader, PdfWriter


def rwcomp(pdf_path):
    output_file = "rwFile.pdf"
    input_pdf = PdfReader(pdf_path)
    output_pdf = PdfWriter()

    for page in input_pdf.pages:
        compressed_stream = page.Stream().compress()
        page.Stream(compressed_stream)
        output_pdf.addpage(page)

    output_pdf.write(output_file)
