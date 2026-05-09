import sys, argparse
import click
from invoice.agent import get_structured_invoice
from invoice.pdf import pdf_extract, write_invoice


@click.group()
def invoice():
    pass


@click.command()
@click.argument("file")
@click.option("--password", help="password to unlock the PDF file.", default="")
def convert(file: str, password: str):
    f = file.removesuffix(".pdf")
    raw_inv = pdf_extract(f"{f}", password=password)
    struct_inv = get_structured_invoice(raw_inv)
    write_invoice(f, struct_inv)

    click.echo(struct_inv)


invoice.add_command(convert)
