import logging

import coupon_validating_system.configuration as config


def setup_logger():
    try:
        logger = logging.getLogger(config.MODULE_NAME)
        logger.setLevel(config.LOGGING_LEVEL)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(config.MODULE_NAME + '.log', mode='w')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    except Exception:
        raise
