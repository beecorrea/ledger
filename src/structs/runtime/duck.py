import duckdb


class DuckRuntime:
    def __init__(self) -> None:
        self.context = duckdb.connect(database="spends.duckdb")
