import polars as pl
import src.models.category as category
import duckdb


class Categorizer:
    def __init__(self, category: category.Category) -> None:
        self.category = category

    def query(self, db):
        statement = "SELECT * FROM root WHERE LOWER(title) LIKE '{}%' ORDER BY amount DESC".format(
            self.category.prefix
        )

        return (
            db.execute(
                statement,
            )
            .pl()
            .with_columns(pl.lit(self.category.name).alias("category"))
        )

    def persist(self, db, df):
        return db.execute(
            """
            MERGE INTO categorized
                USING (SELECT * FROM df) as new
                USING (date, title, amount, category)
                WHEN MATCHED THEN UPDATE
                WHEN NOT MATCHED THEN INSERT;
            """
        )

    def export(self, db: duckdb.DuckDBPyConnection):
        df = db.execute(
            "SELECT * FROM categorized WHERE category = ? and LOWER(title) LIKE '{}%'".format(
                self.category.prefix
            ),
            [self.category.name],
        ).pl()

        return df.write_csv("data/{}.csv".format(self.category.id()))

    def create_table(self, db):
        return db.sql(
            "CREATE TABLE IF NOT EXISTS categorized (date date, title varchar, amount double, category varchar);"
        )
