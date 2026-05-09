# Ledger

**Ledger** automates **data ingestion, processing and analytics** for financial transactions, empowering the user to build a **personal ledger**.

With `ledger`, you can convert invoice PDF filweas to structured data formats (e.g. CSV, Parquet), allowing you to query your spends using an analytical engine such as [DuckDB](https://duckdb.org), allowing you to programatically manage and automate your finances.

# Use Cases
* Building the history of personal financial transactions.
* Creating analyticial reports and dashboards of spends.
* Managing household spends and splitting costs between members.

# Running
```
# Install as a tool to use it from the command line:
uv tool install -e .

# Pass
ledger invoice convert september-invoice.pdf --password s3cretp4ssw0rd
```
