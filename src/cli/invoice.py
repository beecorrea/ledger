import sys

import click
import duckdb
from invoice.agent import get_structured_invoice
from invoice.logic import pdf_extract, write_invoice


@click.group()
def invoice():
    pass


@invoice.command()
@click.option(
    "-p",
    "--pdf",
    help="path to a PDF file containing the invoice.",
    required=True,
)
@click.option(
    "--password",
    help="password to unlock the PDF file.",
    prompt=True,
    hide_input=True,
    default="",
)
def create(pdf: str, password: str):
    """Converts a PDF invoice to CSV."""
    f = pdf.removesuffix(".pdf")
    raw_inv = pdf_extract(f"{f}", password=password)
    struct_inv = get_structured_invoice(raw_inv)
    write_invoice(f, struct_inv)

    click.echo(struct_inv)


@invoice.command()
@click.option("--sql", required=False)
@click.option("--file", required=False)
@click.option("--param", type=(str, str), multiple=True)
def query(sql: str, file: str, param):
    """Queries a CSV file using DuckDB."""
    # Mutual exclusive but one is required
    if (sql is not None and file is not None) or (sql is None and file is None):
        click.echo("must use one of: --sql, --file.")
        sys.exit(1)

    if file is not None:
        f = open(file)
        sql = f.read()
        f.close()

    result = duckdb.sql(query, params=dict(param))
    click.echo(result)
