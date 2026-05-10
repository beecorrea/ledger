import warnings
from langchain_core._api.deprecation import LangChainPendingDeprecationWarning

warnings.filterwarnings(
    "ignore",
    category=LangChainPendingDeprecationWarning,
    message=".*allowed_objects.*",
)

import click
from cli.invoice import invoice


@click.group()
def main():
    pass


if __name__ == "__main__":
    main()

main.add_command(invoice)
