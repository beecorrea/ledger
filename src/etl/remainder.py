import duckdb
import polars as pl


class Remainder:
    def __init__(self) -> None:
        pass

    def query(self, db):
        statement = """
            SELECT * 
            FROM spends.ledger_struct 
            WHERE id NOT IN (
                SELECT DISTINCT id FROM spends.categories WHERE tx_category != ''
            ) AND tx_amount > 0 
            ORDER BY 
                tx_amount DESC,
                tx_title ASC;
        """

        df = (
            db.execute(
                statement,
            )
            .pl()
            .with_columns(pl.lit("").alias("tx_category"))
        )
        return df

    def persist(self, db, df):
        return db.execute(
            """
            MERGE INTO spends.categories
                USING (SELECT * FROM df)
                USING (
                    id,
                    tx_date,
                    tx_amount,
                    tx_title,
                    tx_category
                )
                WHEN MATCHED THEN UPDATE
                WHEN NOT MATCHED THEN INSERT;
            """
        )

    def export(self, db: duckdb.DuckDBPyConnection):
        df = db.execute("SELECT * FROM spends.categories WHERE tx_category = ''").pl()

        return df.write_csv("data/others.csv")
