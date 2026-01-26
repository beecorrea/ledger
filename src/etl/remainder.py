import polars as pl

from src.structs.model import Model
from src.structs.runtime.duck import DuckRuntime


class Remainder(Model):
    def __init__(self, rt: DuckRuntime) -> None:
        super().__init__(kind="remainder", rt=rt)

    def read(self):
        return """
            SELECT * 
            FROM spends.ledger_struct 
            WHERE id NOT IN (
                SELECT DISTINCT id FROM spends.categories WHERE tx_category != ''
            ) AND tx_amount > 0 
            ORDER BY 
                tx_amount DESC,
                tx_title ASC;
        """

    def transform(self, df):
        df = df.with_columns(pl.lit("").alias("tx_category"))

        return df

    def write(self) -> str:
        return """
            INSERT OR IGNORE INTO spends.categories (id, tx_date, tx_amount, tx_title, tx_category) 
            SELECT id, tx_date, tx_amount, tx_title, tx_category FROM df;
        """

    def export(self):
        df = self.rt.context.execute(
            "SELECT * FROM spends.categories WHERE tx_category = ''"
        ).pl()

        return df.write_csv("data/others.csv")
