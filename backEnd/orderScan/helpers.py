from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path


def save_error_pages(save_location: Path, input_pdf: Path, page_indices: list[int]):
    """Gets specific pages by index of a given pdf ans save them
    Is used to gather all menu lists that went wrong

    Args:
        input_pdf (Path): Pdf you want to extract pages from
        page_indices (list[int]): Pages you wan to extract
    """

    output_pdf = save_location / f"FOUT_{input_pdf.name}"

    with open(input_pdf, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)

        pdf_writer = PdfWriter()

        pdf_writer.append(pdf_reader, page_indices)

        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)
