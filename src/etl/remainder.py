import duckdb
import polars as pl


class Remainder:
    def __init__(self) -> None:
        pass

    def query(self, db):
        statement = "select * from root where title not in (select title from categorized where category != '') and amount > 0 order by amount desc, title asc"

        df = (
            db.execute(
                statement,
            )
            .pl()
            .with_columns(pl.lit("").alias("category"))
        )
        return df

    def persist(self, db, df):
        return db.execute(
            """
            MERGE INTO categorized
                USING (SELECT * FROM df)
                USING (date, title, amount, category)
                WHEN MATCHED THEN UPDATE
                WHEN NOT MATCHED THEN INSERT;
            """
        )

    def export(self, db: duckdb.DuckDBPyConnection):
        df = db.execute("SELECT * FROM categorized WHERE category = ''").pl()

        return df.write_csv("data/others.csv")
