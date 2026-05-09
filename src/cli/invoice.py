import sys, argparse
import click
from invoice.agent import get_structured_invoice
from invoice.pdf import pdf_extract, write_invoice


@click.group()
def invoice():
    pass


@click.command()
@click.argument("file")
@click.option("--pasword", help="password to unlock the PDF file.", default="")
def convert(f: str, password: str):
    f = f.removesuffix(".pdf")
    # raw_inv = pdf_extract(f"{f}", password=password)
    struct_inv = "hello!"
    # struct_inv = get_structured_invoice(raw_inv)
    # write_invoice(f, struct_inv)

    click.echo(struct_inv)


def make_cli():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "name",
        help="name of the PDF file to extract text from.",
        type=str,
    )
    parser.add_argument(
        "-p",
        "--password",
        help="password to unlock the PDF file.",
        type=str,
        default="",
    )

    return parser


invoice.add_command(convert)
