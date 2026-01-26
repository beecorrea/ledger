import polars as pl
import src.models.category as category
import duckdb


class Categorizer:
    def __init__(self, category: category.Category) -> None:
        self.category = category

    def query(self, db):
        statement = "SELECT * FROM spends.ledger_raw WHERE LOWER(tx_title) LIKE '{}%' ORDER BY tx_amount DESC".format(
            self.category.prefix
        )

        return (
            db.execute(
                statement,
            )
            .pl()
            .with_columns(pl.lit(self.category.name).alias("tx_category"))
        )

    def persist(self, db, df):
        return db.execute(
            """
            MERGE INTO spends.categories
                USING (SELECT * FROM df) as new
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
        df = db.execute(
            """
                SELECT * 
                FROM spends.categories 
                WHERE tx_category = ? AND LOWER(tx_title) LIKE '{}%';
            """.format(
                self.category.prefix
            ),
            [self.category.name],
        ).pl()

        return df.write_csv("data/{}.csv".format(self.category.id()))

    def create_table(self, db):
        return db.sql(
            """
                CREATE TABLE IF NOT EXISTS spends.categories (
                    id UBIGINT PRIMARY KEY,
                    tx_date DATE,
                    tx_amount DOUBLE,
                    tx_title VARCHAR,
                    tx_category VARCHAR
                );
            """
        )
