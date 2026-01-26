import duckdb
from abc import abstractmethod
from polars import DataFrame
from src.structs.runtime.duck import DuckRuntime


class Model:
    def __init__(self, rt: DuckRuntime, kind: str) -> None:
        self.rt = rt
        self.kind = kind

    """
    ########## Model Core ###########
    Main functions used by the runtime.
    """

    def query(self) -> DataFrame:
        q = self.read()
        pl = self.rt.context.execute(q).pl()

        return pl

    def persist(self, df: DataFrame) -> duckdb.DuckDBPyConnection:
        df = self.transform(df)
        q = self.write()

        return self.rt.context.execute(q)

    """
    ########## Model API ###########
    Must be implemented by client (i.e. concrete Model).
    Used by the core to perform logic.
    """

    @abstractmethod
    ## TODO: derive from schema
    def create_table(self) -> duckdb.DuckDBPyConnection:
        pass

    @abstractmethod
    def read(self) -> str:
        """
        Reads data from a table.
        """
        pass

    @abstractmethod
    def write(self) -> str:
        """
        Reads data from a table.
        """
        pass

    @abstractmethod
    def transform(self, df: DataFrame) -> DataFrame:
        """
        Applies transformations to dataframe.
        """
        pass
