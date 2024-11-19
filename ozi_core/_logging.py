from __future__ import annotations

import gzip
import json
import logging
import logging.handlers
from pathlib import Path

from platformdirs import user_log_dir

LOG_PATH = Path(user_log_dir('OZI')) / 'log.txt'
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self: CompressedRotatingFileHandler) -> None:  # pragma: no cover
        super().doRollover()
        with gzip.open(f'{self.baseFilename}.gz', 'wb') as f:
            f.write(Path(self.baseFilename).read_bytes())
        Path(self.baseFilename).write_text('')


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        json.dumps(
            {
                'time': '%(asctime)-s',
                'level': '%(levelname)-s',
                'module': '%(module)-s',
                'funcName': '%(funcName)-s',
                'message': '%(message)s',
            }
        )
        + ','
    )
    handler = CompressedRotatingFileHandler(
        LOG_PATH,
        maxBytes=1_000_000,
        backupCount=5,
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
