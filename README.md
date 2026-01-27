# Ledger: DuckDB-powered personal ledger

**Ledger** automates **data ingestion, processing and analytics** for financial transactions, empowering the user to build a **personal ledger**.

**Ledger** uses DuckDB's OLAP engine to ingest raw CSV files and categorize transactions into a structured table. Then, you can run **analytical queries** of your spends in a friendly way, allowing you to **optimize and manage your spends**.

# Use Cases
* Building the history of personal financial transactions.
* Managing household spends and splitting costs between members.
* Building reports and dashboards of your spends.

# Running
Please check the [Setup](#setup) section to properly configure your **Ledger** instance
```
uv install

uv run main.py
```
# Setup
Ledger uses a YAML [configuration file](ledger.example.yaml) to setup the required initial parameters. You can swap the values there to configure Ledger as desired.

## Ingestion Targets (table: ledger_struct)
**Ingestion Targets** are CSV files that contains a list of transactions. For Ledger to work properly, Targets must use the following format:
```csv
date,title,amount
2025-12-28,Burger King,45.88
2025-12-28,Amazon,151.86
2025-12-28,Uber,13.81
2025-12-28,Metrô,45.88
2025-12-28,Vivo,70.99
```

## Categories (table: categories)
A **Category** classifies a transaction matches a transaction's title to a user-defined search prefix. In the previous example, if we had a category named `food` with a key `burger`, the final classification would be:
```csv
date,title,amount,category
2025-12-28,Burger King,45.88,food
2025-12-28,Amazon,151.86,
2025-12-28,Uber,13.81,
2025-12-28,Metrô,45.88,
2025-12-28,Vivo,70.99,
```

### Creating new Categories
**Categories** are extensible, and as your spending habits change you can add new categories or remove old ones!

Notice that *unmatched transactions aren't categorized* and require an individual analysis strategy to understand the transaction and further classify it. 

In the previous example, one can see that there's a potential category called `transportation`, with keys `uber` and `metro`: 
```csv
date,title,amount,category
2025-12-28,Burger King,45.88,food
2025-12-28,Amazon,151.86,
2025-12-28,Uber,13.81,transportation
2025-12-28,Metrô,45.88,transportation
2025-12-28,Vivo,70.99,
```
