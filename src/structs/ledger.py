import yaml
from loguru import logger


class Ledger:
    """
    Manages Ledger declarations such as input_files
    """

    def __init__(self, cfg: str = "ledger.yaml") -> None:
        with open(cfg) as f:
            self.ledger = yaml.safe_load(f)
        self.database = self.ledger["database"]
        self.ingestion = self.ledger["ingestion"]
        self.categories = self.ledger["categories"]
        logger.info("{}", self.ledger)
