# import sys

# sys.path.append('/Users/jakob/.pyenv/versions/3.9.1/lib/python3.9/site-packages')
from io import BytesIO
from time import perf_counter
from pdf2image import convert_from_path
from PIL import Image
from backEnd.orderScan.menu_list import MenuList
from backEnd.dataClasses.customErrors import OrderScanError
from backEnd.orderScan.constants import OrderScanCsv
from pandas import DataFrame, concat
from pathlib import Path
from backEnd.orderScan.helpers import save_error_pages
from backEnd.gtHelpers import saveAsCsv
from logging import Logger


def processMenulists(pdfLocation: Path, exportFolder: Path) -> str:
    """Given a pdf with menu lists, retrieve all the needed information to make orders which are exportable to Exact
    Menu lists that get an error are saved to a seperate pdf and a log is recorded wy they fail

    Args:
        pdfLocation (Path): Location of pdf you want to read
        exportFolder (Path): Place where the resulting csv and error pdf will be droppped

    Returns:
        str: The log of what went wrong
    """

    errorLog = "Bij de volgende menulijsten konden de orders niet worden opgehaald:\n"
    all_orders = DataFrame(columns=OrderScanCsv.CSV_COLUMNS)
    incorrect_pages = []
    incorrect_page_counter = 1

    tik = perf_counter()
    pages = convert_from_path(pdfLocation, fmt="jpeg", dpi=400)
    print(f"Finished reading {len(pages)} pages in {perf_counter() - tik:.2f}s")

    for index, page in enumerate(pages):
        # if index == 2 - 1:
        tik_tik = perf_counter()
        # Use writer to not save image during intermediate step
        with BytesIO() as f:
            page.save(f, format="jpeg")
            f.seek(0)
            pil_image = Image.open(f)

            # Get the orders for a given page, if something goes wrong save why to the log and go to next page
            try:
                menu_list = MenuList(
                    pil_image,
                    plot_get=False,
                    plot_orders=False,
                    plot_client_id=False,
                    plot_meta_data=False,
                )
                all_orders = concat(
                    [all_orders, menu_list.orders_df], ignore_index=True
                )

            # Made several custom error messages depending on were something goes wrong
            except Exception as error:
                errorLog += f"Pagina {incorrect_page_counter}: {error}\n"
                print(f"page {index +1}: {error}\n")
                incorrect_pages.append(index)
                incorrect_page_counter += 1

            print(
                f"Finished page {index +1} of {len(pages)} in {perf_counter() - tik_tik:.2f}s"
            )

    # Save the pages with errors as a new pdf
    if len(incorrect_pages) > 0:
        save_error_pages(exportFolder, pdfLocation, incorrect_pages)

    if len(all_orders) > 0:
        # Strip everything but the original pdf name
        pdf_name = pdfLocation.name.rstrip(".pdf")
        saveAsCsv(exportFolder, all_orders, pdf_name)

    log = "\n\n====== RESULTATEN ======\n"
    log += f"{len(pages)} pagina's uitgelezen met in totaal {len(all_orders)} maaltijden in {int(perf_counter() - tik)} seconden\n\n"
    log += errorLog
    return log
