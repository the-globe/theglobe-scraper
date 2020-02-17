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
        except Exception:
            self.logger.error('An Error araised', exc_info=True)
        else:
            self.logger.info('Database initialized')

    def _insert_many_articles_(self, documents):
        """DOCUMENT STRUCTURE: {'articles': [{document},{document},{document}]}"""
        try:
            # w_0 = collection.with_options(write_concern=WriteConcern(w=0))
            self.logger.debug(f"Try to insert {len(documents['articles'])} articles.")
            result = self.collection.insert_many(documents['articles'], ordered = False)
        except BulkWriteError as bwe:

            duplicated_docs = 0
            for item in bwe.details['writeErrors']: # Only throws an error if error code is not 11000 (11000 = duplicate)
                if item['code'] != 11000:
                    self.logger.error(f"{type(bwe)} -> 'index': {item['index']},'code': {item['code']}, 'errmsg': {item['errmsg']}")
                else:
                    duplicated_docs += 1

            list_details = []
            for item in ['writeConcernErrors', 'nInserted', 'nUpserted', 'nMatched', 'nModified', 'nRemoved', 'upserted']:
                list_details.append(f"{item}: {bwe.details[item]}")
            self.logger.debug(list_details)

            self.logger.info(f"Inserted documents: {bwe.details['nInserted']}")
            self.logger.debug(f"Duplicated documents: {duplicated_docs}")
            self.logger.debug(f"Failed documents: {len(documents['articles']) - bwe.details['nInserted'] - duplicated_docs}")
        else:
            self.logger.info(f"Inserted documents: {len(result.inserted_ids)}")