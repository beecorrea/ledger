class Ingestor:
    def __init__(self, target) -> None:
        # Target file to be ingested.
        self.target = target
        pass

    def ingest_csv(self, db):
        resolved = "{}/{}.csv".format("data", self.target)
        stmt = "CREATE OR REPLACE TABLE root AS FROM read_csv('{}');".format(resolved)
        return db.execute(stmt)
