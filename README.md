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

# Convert a invoice PDF to a structured CSV file. 
# The generated CSV file will have the same name as the PDF file.
ledger invoice create --pdf september-invoice.pdf --password s3cretp4ssw0rd

# Query an invoice using DuckDB. Good for ad-hoc querying a single invoice.
ledger invoice query --sql "SELECT * FROM 'september-invoice.csv LIMIT 10';"

# Or write the query to a file and run it. Use it when you have a complex query with parameters.
echo "SELECT * FROM 'september-invoice.csv LIMIT $nrows';" > query.sql
ledger invoice query --file query.sql --param nrows 10
```
