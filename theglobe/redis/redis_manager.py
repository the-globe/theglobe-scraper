from redisbloom.client import Client
import logging

class RedisManager():

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        REDIS_HOST = "rdwc.de"
        REDIS_PORT = 6379
        REDIS_PASSWORD = ""

        try:
            self.rb = Client(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
            self.logger.info(f"Successfully connected to redis server")
        except Exception as e:
            self.logger.critical(f"Unable to connect to redis server: {e}")

    def _bf_add_url_(self, url):
        try:
            bf_add = self.rb.bfAdd('bf_urls', url)
            if bf_add:
                self.logger.error(f"Added '{url}' to bloomfilter.")
            else:
                self.logger.error(f"Couln't add '{url}' to bloomfilter")
        except Exception as e:
            self.logger.error(e)

    def _bf_check_url_pres_(self, url):
        if self.rb.bfExists('bf_urls', url):
            self.logger.info(f"Found '{url}' in bloomfilter")
            return True
        else:
            self.logger.debug(f"Coudln't find '{url}' in bloomfilter")
            return False

if __name__ == '__main__':
    rm = RedisManager()
    rm._bf_add_url_("test1")