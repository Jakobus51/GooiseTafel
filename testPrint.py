import os
import tempfile
import win32print
import win32api
import PyPDF2
from backEnd.constants import saveLocations as sl


def print_pdf(pdf_path, printer_name):
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as temp_pdf:
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfFileReader(pdf_file)
            writer = PyPDF2.PdfFileWriter()

            for page_num in range(reader.getNumPages()):
                page = reader.getPage(page_num)
                writer.addPage(page)

            with open(temp_pdf.name, "wb") as temp_file:
                writer.write(temp_file)

        win32api.ShellExecute(0, "print", temp_pdf.name, f'/d:"{printer_name}"', ".", 0)


def select_printer():
    printers = [win32print.GetDefaultPrinter()]
    for printer in win32print.EnumPrinters(
        win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    ):
        printers.append(printer[2])

    print("Available printers:")
    for i, printer in enumerate(printers):
        print(f"{i}: {printer}")

    printer_index = int(input("Select the printer index: "))
    return printers[printer_index]


def main():
    labelFile = "labelTest.pdf"
    labelPath = sl.GotaLabelOutput / labelFile
    printer_name = select_printer()
    print_pdf(labelPath, printer_name)
    print(f"Printing {labelPath} on {printer_name}...")


if __name__ == "__main__":
    main()
