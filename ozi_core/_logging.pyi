import logging
import logging.handlers

LOG_PATH: str

class PytestFilter(logging.Filter):
    def filter(self: PytestFilter, record: logging.LogRecord) -> bool: ...

class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self) -> None: ...

def config_logger() -> None: ...
