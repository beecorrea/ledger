import duckdb
from src.structs.model import Model
from polars import DataFrame


class DuckRuntime:
    """
    Runs a Model step-by-step.
    """

    def __init__(self) -> None:
        self.context = duckdb.connect(database="spends.duckdb")

    def run(self, m: Model):
        print("running", m.kind)
        ct = m.create_table()
        if ct:
            self.context.execute(ct)

        df = self.query(m)
        self.persist(m, df)

        exp = m.export()
        if exp:
            self.context.execute(exp)

    def query(self, m: Model) -> DataFrame:
        q = m.read()
        pl = self.context.execute(q).pl()

        return pl

    def persist(self, m: Model, df: DataFrame) -> duckdb.DuckDBPyConnection:
        df = m.transform(df)
        q = m.write()
        return self.context.execute(q)
