import yaml
import duckdb
from src.structs.model import Model
from polars import DataFrame
from loguru import logger


class DuckRuntime:
    """
    Runs a Model step-by-step.
    """

    def __init__(self, db: str) -> None:
        self.db_name = db
        self.context = duckdb.connect(database="{}.duckdb".format(self.db_name))

    def run(self, m: Model):
        logger.info("kind={}", m.kind)
        ct = m.create_table()
        if ct:
            logger.info("create_table_query={}", m.kind)
            self.context.execute(ct)

        df = self.query(m)
        self.persist(m, df)

        exp = m.export()
        if exp:
            logger.info("export_query={}", exp)
            self.context.execute(exp)

    def query(self, m: Model) -> DataFrame:
        q = m.read()
        logger.info("read_query={}", q)
        pl = self.context.execute(q).pl()

        return pl

    def persist(self, m: Model, df: DataFrame) -> duckdb.DuckDBPyConnection:
        df = m.transform(df)
        q = m.write()
        logger.info("write_query={}", q)
        return self.context.execute(q)
