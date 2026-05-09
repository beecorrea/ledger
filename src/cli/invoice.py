import click
import duckdb
from invoice.agent import get_structured_invoice
from invoice.pdf import pdf_extract, write_invoice


@click.group()
def invoice():
    pass


@click.command()
@click.argument("file")
@click.option(
    "--password",
    help="password to unlock the PDF file.",
    prompt=True,
    hide_input=True,
    default="",
)
def convert(file: str, password: str):
    f = file.removesuffix(".pdf")
    raw_inv = pdf_extract(f"{f}", password=password)
    struct_inv = get_structured_invoice(raw_inv)
    write_invoice(f, struct_inv)

    click.echo(struct_inv)


@click.command()
@click.option("--query", required=False)
@click.option("--file", required=False)
@click.option("--param", type=(str, str), multiple=True)
def query(query: str, file: str, param):
    # Mutual exclusive but one is required
    # if (query != "" and file != "") or (query == "" and file == ""):
    # click.echo("error: must use one of --query and --file")

    if file is not None:
        f = open(file)
        query = f.read()
        f.close()

    param_dict = dict(param)

    result = duckdb.sql(query, params=param_dict)
    click.echo(result)


invoice.add_command(convert)
invoice.add_command(query)
