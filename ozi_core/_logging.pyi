import logging
import logging.handlers

from _typeshed import Incomplete

LOG_PATH: Incomplete

class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self) -> None: ...

def get_logger(name: str) -> logging.Logger: ...
