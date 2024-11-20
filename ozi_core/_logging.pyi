import logging
import logging.handlers
from pathlib import Path

LOG_PATH: Path

class PytestFilter(logging.Filter):
    def filter(self: PytestFilter, record: logging.LogRecord) -> bool: ...

class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self) -> None: ...

def config_logger() -> None: ...
