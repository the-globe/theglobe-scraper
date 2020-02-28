import logging
import os
import json
import logging.config
import colorlog




"""TODO: Set "debug_rotating_file_handler" to only handle DEBUG level logs in logging.json"""
class InitLogging():

        def __init__(self, default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
            logger = logging.getLogger(__name__) # theglobe.logging.init_logging

            dir_path = os.path.dirname(os.path.realpath(__file__)) # Get path of this file

            if not os.path.exists(os.path.join(dir_path, 'tmp')): # Check if tmp folder exist
                os.makedirs(os.path.join(dir_path, 'tmp'))

            config_path = os.path.join(dir_path, default_path)
            value = os.getenv(env_key, None)
            if value:
                config_path = value
            if os.path.exists(config_path):
                with open(config_path, 'rt') as f:
                    config = json.load(f)
                logging.config.dictConfig(config)
                logger.debug(f"Logging Config loaded from file: {config_path}")


            else:
                logging.basicConfig(level=default_level)
                logger.debug(f"Basic Config loaded...")