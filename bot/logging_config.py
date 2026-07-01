import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FILE = "trading_bot.log"
LOG_LEVEL = logging.DEBUG

def setup_logger(name: str) -> logging.Logger:
    """
    Creates and returns a logger that writes to both:
    - Console (INFO and above)
    - File (DEBUG and above — everything)
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    # --- Formatter ---
    # This defines how each log line looks
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # --- File Handler ---
    # Writes everything (DEBUG+) to trading_bot.log
    # Max 5MB per file, keeps last 3 files (so logs don't grow forever)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # --- Console Handler ---
    # Only shows INFO and above in terminal (not noisy DEBUG lines)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Attach both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

