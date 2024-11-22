from __future__ import annotations

import gzip
import json
import logging
import logging.handlers
import os
import sys
from pathlib import Path

from platformdirs import user_log_dir

LOG_PATH = Path(user_log_dir('OZI')) / 'log.json'
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)


class PytestFilter(logging.Filter):
    def filter(self: PytestFilter, record: logging.LogRecord) -> bool:  # pragma: no cover
        return os.environ.get('PYTEST_VERSION') is None or 'pytest' not in sys.modules


class CompressedRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def doRollover(self: CompressedRotatingFileHandler) -> None:  # pragma: no cover
        super().doRollover()
        with gzip.open(f'{self.baseFilename}.gz', 'wb') as f:
            f.write(Path(self.baseFilename).read_bytes())
        Path(self.baseFilename).write_text('')


def config_logger() -> None:
    logger = logging.getLogger('ozi_core')
    logger.propagate = False
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        json.dumps(
            {
                'time': '%(asctime)-s',
                'level': '%(levelname)-s',
                'logger': '%(name)s',
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
    logger.addFilter(PytestFilter())
