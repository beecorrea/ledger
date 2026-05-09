import csv

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c


def pdf_extract(name: str, password="") -> str:
    pdf = pdfium.PdfDocument(f"{name}.pdf", password)

    n_pages = len(pdf)
    text_all = []

    for i in range(n_pages):
        page = pdf[i]
        page_text = page.get_textpage().get_text_bounded()
        text_all.append(page_text)

    return "\n".join(text_all)


def write_invoice(name: str, invoice: str):
    with open(f"{name}.csv", "w") as f:
        f.write(invoice)
        f.close()
