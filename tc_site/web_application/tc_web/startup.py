import os
from tc_web import config
import time_candle.app_logger


# on server start check our base folder or create it
def start_up():
    if not os.path.exists(config.BASE_DIR):
        os.makedirs(config.BASE_DIR)
    time_candle.app_logger.setup_logging(
        enabled=config.ENABLED,
        log_conf=config.LOG_CONF_PATH)
