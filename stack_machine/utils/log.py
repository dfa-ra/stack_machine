import logging
from logging.handlers import RotatingFileHandler

from stack_machine.config.config import log_file

logger = logging.getLogger("stack_machine")

handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=5)
handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)