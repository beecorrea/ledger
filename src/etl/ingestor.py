from src.structs.model import Model
import polars as pl


class Ingestor(Model):
    def __init__(self, target) -> None:
        super().__init__(kind="ingestor")
        self.target = target

    def create_table(self):
        return """
            CREATE TABLE IF NOT EXISTS spends.ledger_struct (
                id UBIGINT PRIMARY KEY,
                tx_date DATE,
                tx_amount DOUBLE,
                tx_title VARCHAR
            );
        """

    def read(self) -> str:
        resolved = "{}/{}.csv".format("data", self.target)
        stmt = "SELECT * FROM read_csv('{}');".format(resolved)

        return stmt

    def write(self) -> str:
        return """
            INSERT OR IGNORE INTO spends.ledger_struct (id, tx_date, tx_amount, tx_title) 
            SELECT id, tx_date, tx_amount, tx_title FROM df;
        """

    def transform(self, df: pl.DataFrame) -> pl.DataFrame:
        df = df.with_columns(
            pl.concat_str(["amount", "date", "title"]).hash().alias("id")
        )

        df = df.rename({"amount": "tx_amount", "date": "tx_date", "title": "tx_title"})

        return df
