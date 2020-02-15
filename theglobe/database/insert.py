# database/insert.py

from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo import WriteConcern
from pprint import pprint

import logging
import os
import json


class Insert():
    def __init__(self, url, db, collection, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        try:
            self.client = MongoClient(url)
            self.db = self.client[db]
            self.collection = self.db[collection]
        except Exception as exception:
            self.logger.error('An Error araised', exc_info=True)
        else:
            self.logger.info('Database initialized')
    

    def _insert_many_articles_(self, documents):
        """DOCUMENT STRUCTURE: {'articles': [{document},{document},{document}]}"""
        try:
            # w_0 = collection.with_options(write_concern=WriteConcern(w=0))
            self.logger.info(f"Try to insert {len(documents['articles'])} articles.")
            result = self.collection.insert_many(documents['articles'], ordered = False)
        except BulkWriteError as bwe:
            self.logger.warning(f"Insert error accured: {bwe} {type(bwe)}")

            list_failed_inserts = []
            for item in bwe.details['writeErrors']:
                item = [item['index'],item['op']['_id']]
                list_failed_inserts.append(item)
            self.logger.warning(f"{list_failed_inserts}")

            list_of_details = []
            for item in ['writeConcernErrors', 'nInserted', 'nUpserted', 'nMatched', 'nModified', 'nRemoved', 'upserted']:
                list_of_details.append(f"{item}:{bwe.details[item]}")
            self.logger.warning(f"{list_of_details}")

            self.logger.info(f"Inserted documents: {bwe.details['nInserted']}")
            self.logger.info(f"Failed documents: {len(documents['articles']) - bwe.details['nInserted']}")
        else:
            self.logger.info(f"Inserted documents: {len(result.inserted_ids)}")