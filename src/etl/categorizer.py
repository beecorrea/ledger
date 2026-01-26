from src.structs.runtime.duck import DuckRuntime
from src.structs.model import Model
from src.structs.category import Category
import polars as pl


class Categorizer(Model):
    def __init__(self, rt: DuckRuntime, category: Category) -> None:
        super().__init__(kind="categorizer", rt=rt)

        self.category = category

    def create_table(self):
        stmt = """
                CREATE TABLE IF NOT EXISTS spends.categories (
                    id UBIGINT PRIMARY KEY,
                    tx_date DATE,
                    tx_amount DOUBLE,
                    tx_title VARCHAR,
                    tx_category VARCHAR
                );
            """

        return self.rt.context.execute(stmt)

    def read(self) -> str:
        stmt = "SELECT * FROM spends.ledger_struct WHERE LOWER(tx_title) LIKE '{}%' ORDER BY tx_amount DESC".format(
            self.category.prefix
        )

        return stmt

    def write(self) -> str:
        return """
            INSERT OR IGNORE INTO spends.categories (id, tx_date, tx_amount, tx_title, tx_category) 
            SELECT id, tx_date, tx_amount, tx_title, tx_category FROM df;
        """

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns(pl.lit(self.category.name).alias("tx_category"))

        return df

    def export(self):
        stmt = """
                SELECT * 
                FROM spends.categories 
                WHERE tx_category = ? AND LOWER(tx_title) LIKE '{}%';
            """.format(
            self.category.prefix
        )
        df = self.rt.context.execute(
            stmt,
            [self.category.name],
        ).pl()

        return df.write_csv("data/{}.csv".format(self.category.id()))
