import duckdb


class DuckRuntime:
    def __init__(self) -> None:
        self.conn = duckdb.connect(database="spends.duckdb")
