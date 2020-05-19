import logging
from src.includes.colored_logger import ColoredLogger


def setup_logger(name, use_color=True):
    logger = logging.getLogger()
    return ColoredLogger(name, logger.level, use_color)
