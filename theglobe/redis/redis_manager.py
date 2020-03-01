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
        except Exception as e:
            self.logger.critical(f"Unable to connect to redis server: {e}")

    def hello_redis(self):
        try:

            print(self.rb.bfCreate('bloom', 0.01, 1000))
            print(self.rb.bfAdd('bloom', 'test'))

        except Exception as e:
            self.logger.error(e)


if __name__ == '__main__':
    rm = RedisManager()
    rm.hello_redis()