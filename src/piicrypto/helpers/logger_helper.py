import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(
    log_dir: str = "logs",
    base_filename: str = "piicrypto",
    name: str = None,
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
        )

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"{base_filename}_{timestamp}.log")

        rotating_handler = RotatingFileHandler(
            log_file, mode="a", maxBytes=max_bytes, backupCount=backup_count
        )
        rotating_handler.setFormatter(formatter)
        logger.addHandler(rotating_handler)

        logger.propagate = False

    return logger
