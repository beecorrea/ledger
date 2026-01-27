import duckdb
from abc import abstractmethod
from polars import DataFrame


class Model:
    def __init__(self, kind: str) -> None:
        self.kind = kind

    """
    ########## Model API ###########
    Must be implemented by client (i.e. concrete Model).
    Used by the core to perform logic.
    """

    @abstractmethod
    ## TODO: derive from schema
    def create_table(self) -> str:
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

    @abstractmethod
    def export(self) -> str:
        """
        Applies transformations to dataframe.
        """
        pass
