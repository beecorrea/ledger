import src.models.category as category
import src.etl.categorizer as categorizer
import src.etl.remainder as remainder
import src.etl.ingestor as ingestor
import src.runtime.duck as duck


def main():
    d = duck.DuckRuntime()
    db = d.conn

    # Setup ingestion table
    ing = ingestor.Ingestor("2026-01")
    ing.table_raw_ledger(db)
    txs = ing.query(db)
    ing.persist(db, txs)

    # For each category in the ledger:
    for cat in category.build_categories():
        categ = categorizer.Categorizer(cat)

        # Initialize the table if needed
        categ.create_table(db)

        # Get rows for the current category
        res = categ.query(db)

        # Add categorized rows to the ledger
        categ.persist(db, res)

        # Export to csv
        categ.export(db)

    rem = remainder.Remainder()
    rem.persist(db, rem.query(db))
    rem.export(db)


if __name__ == "__main__":
    main()
