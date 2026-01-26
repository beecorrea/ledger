import src.structs.category as category
import src.etl.categorizer as categorizer
import src.etl.remainder as remainder
import src.etl.ingestor as ingestor
import src.structs.runtime.duck as duck


def main():
    d = duck.DuckRuntime()
    db = d.context

    # Setup ingestion table
    ing = ingestor.Ingestor(d, "2026-01")
    db = ing.create_table()
    txs = ing.query()
    db = ing.persist(txs)

    # For each category in the ledger:
    for cat in category.build_categories():
        categ = categorizer.Categorizer(d, cat)

        # Initialize the table if needed
        categ.create_table()

        # Get rows for the current category
        res = categ.query()

        # Add categorized rows to the ledger
        categ.persist(res)

        # Export to csv
        categ.export()

    # Calculate remainder table
    rem = remainder.Remainder()
    rem.persist(db, rem.query(db))
    rem.export(db)


if __name__ == "__main__":
    main()
