import polars as pl
from datetime import datetime


class Ingestor:
    def __init__(self, target) -> None:
        # Target file to be ingested.
        self.target = target

    def table_raw_ledger(self, db):
        stmt = """
            CREATE TABLE IF NOT EXISTS spends.ledger_struct (
                id UBIGINT PRIMARY KEY,
                tx_date DATE,
                tx_amount DOUBLE,
                tx_title VARCHAR
            );
        """

        return db.execute(stmt)

    def query(self, db):
        resolved = "{}/{}.csv".format("data", self.target)
        stmt = "SELECT * FROM read_csv('{}');".format(resolved)
        return db.execute(stmt).pl()

    def persist(self, db, df: pl.DataFrame):
        df = df.with_columns(
            pl.concat_str(["amount", "date", "title"]).hash().alias("id")
        )

        df = df.rename({"amount": "tx_amount", "date": "tx_date", "title": "tx_title"})

        return db.execute(
            """
            INSERT OR IGNORE INTO spends.ledger_struct (id, tx_date, tx_amount, tx_title) 
            SELECT id, tx_date, tx_amount, tx_title FROM df;
            """.format(
                self.target
            )
        )
