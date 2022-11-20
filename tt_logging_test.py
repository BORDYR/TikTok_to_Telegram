import logging
from logger_config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('TTtoTG_logger')

for i in range(1000):
	logger.info(f'info log {i}')