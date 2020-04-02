from redisbloom.client import Client
import logging

class RedisManager(object):

    def __init__(self, settings, stats):
        self.logger = logging.getLogger(__name__)
        self.settings = settings
        self.stats = stats

        REDIS_HOST = self.settings.get('REDIS_HOST')
        REDIS_PORT = self.settings.get('REDIS_PORT')
        REDIS_PASSWORD = self.settings.get('REDIS_PASSWORD')

        try:
            self.rb = Client(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
            self.logger.info(f"Successfully connected to redis server")
        except Exception as e:
            self.logger.error(f"Unable to connect to redis server: {e}")


    def _bf_add_url_(self, url):
        try:
            bf_add = self.rb.bfAdd('bf_urls', url)
            if bf_add:
                self.stats.inc_value('redis/bloomfilter/added_urls')
                self.logger.info(f"Added '{url}' to bloomfilter.")
            else:
                self.logger.error(f"Couldn't add '{url}' to bloomfilter")
        except Exception as e:
            self.logger.error(e)

    def _bf_check_url_pres_(self, url):
        if self.rb.bfExists('bf_urls', url):
            self.logger.debug(f"Found '{url}' in bloomfilter")
            self.stats.inc_value('redis/bloomfilter/existing_urls')
            return True
        else:
            self.logger.debug(f"Couldn't find '{url}' in bloomfilter")
            self.stats.inc_value('redis/bloomfilter/not_existing_urls')
            return False

# if __name__ == '__main__':
#     rm = RedisManager()
#     rm._bf_add_url_("test1")