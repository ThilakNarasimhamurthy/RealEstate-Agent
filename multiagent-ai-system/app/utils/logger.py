# utils/logger.py
import logging

# Configure logging once, the first time this file is imported
logging.basicConfig(
    level=logging.INFO,                     # default level = INFO
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)

def get_logger(name: str | None = None) -> logging.Logger:
    """
    Grab a ready-to-use logger:
        logger = get_logger(__name__)
    """
    return logging.getLogger(name)
