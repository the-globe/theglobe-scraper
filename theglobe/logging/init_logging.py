import logging
import os
import json
import logging.config
import colorlog


"""TODO: Set "debug_rotating_file_handler" to only handle DEBUG level logs in logging.json"""
class InitLogging():

        def __init__(self, default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
            logger = logging.getLogger(__name__)
            """Setup logging configuration

            """
            dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), default_path)
            value = os.getenv(env_key, None)
            if value:
                path = value
            if os.path.exists(dir_path):
                with open(dir_path, 'rt') as f:
                    config = json.load(f)
                logging.config.dictConfig(config)
                logger.debug(f"Logging Config loaded from file: {dir_path}")


            else:
                logging.basicConfig(level=default_level)
                logger.debug(f"Basic Config loaded...")