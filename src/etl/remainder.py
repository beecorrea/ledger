import polars as pl
from src.structs.model import Model


class Remainder(Model):
    def __init__(self) -> None:
        super().__init__(kind="remainder")

    def read(self):
        return """
            SELECT * 
            FROM ledger_struct 
            WHERE id NOT IN (
                SELECT DISTINCT id FROM categories WHERE tx_category != ''
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
            INSERT OR IGNORE INTO categories (id, tx_date, tx_amount, tx_title, tx_category) 
            SELECT id, tx_date, tx_amount, tx_title, tx_category FROM df;
        """

    def export(self):
        return """
            COPY (
                SELECT * 
                FROM categories 
                WHERE tx_category = ''
            ) TO 'data/others.csv' (HEADER, DELIMITER ',');
        """
