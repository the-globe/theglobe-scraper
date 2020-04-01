# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json
import logging
from pymongo.errors import BulkWriteError
from pymongo.errors import DuplicateKeyError
from pymongo import WriteConcern

class TheglobePipeline(object):

    def process_item(self, item, spider):
        return item


class MongoPipeline(object):

    def __init__(self, mongo_url, mongo_db, mongo_coll, stats):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll
        self.logger = logging.getLogger(__name__)
        self.stats = stats


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_url = crawler.settings.get('MONGO_URL'),
            mongo_db = crawler.settings.get('MONGO_DATABASE'),
            mongo_coll = crawler.settings.get('MONGO_COLLECTION'),
            stats = crawler.stats
        )


    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_url)
            self.db = self.client[self.mongo_db]
            self.collection = self.db[self.mongo_coll]
        except Exception:
            self.logger.error('An Error araised', exc_info=True)
        else:
            self.logger.info('Database initialized')


    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        try:
            # w_0 = collection.with_options(write_concern=WriteConcern(w=0))
            self.logger.debug(f"Try to insert item")
            result = self.collection.insert_one(dict(item))
        except DuplicateKeyError:
            self.logger.debug("Document already exist!")
            self.stats.inc_value('mongodb/duplicated_documents')
        except Exception:
            self.logger.error("Error araised while trying to insert a document", exc_info=True)
            self.stats.inc_value('mongodb/failed_documents')
        else:
            self.logger.debug("Document inserted")
            self.logger.debug(f"Result: {result}")
            self.stats.inc_value('mongodb/inserted_documents')
        return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # line = json.dumps(dict(item)) + "\n"
        line = str(item) + "\n"
        self.file.write(line)
        return item