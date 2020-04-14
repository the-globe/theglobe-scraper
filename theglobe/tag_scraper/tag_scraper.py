import requests
from pprint import pprint
import os

import concurrent.futures
import itertools

from pymongo import MongoClient
import logging



class __TagScraper__(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        self.MONGO_URL = 'mongodb://rdwc.de:27017/'
        self.MONGO_DATABASE = 'tg'
        self.MONGO_COLLECTION = 'articles-testing'
        self.MAX_CONCURRENT_CONTENT = 50

        self.AZURE_SUBSCRIPTION_KEY = "267a1a7a40074ebdb92cf5a91dde1f74"
        self.AZURE_ENDPOINT = "shttps://theglobe-text-analysis.cognitiveservices.azure.com/"

        self.content_gen = self.__content_generator_()


    def __content_generator_(self):
        client = MongoClient(self.MONGO_URL)
        db = client[self.MONGO_DATABASE]
        collection = db[self.MONGO_COLLECTION]
        cursor = collection.find({"tagged": False, "content": { "$nin": ["", "N/A"]}})

        for article in cursor:
            if len(article['content']) > 5000:
                self.logger.warning(f"Article {article['url']} contains more than 5000 characters and is too long for an azure document!")
            yield article['content'], article['url']

    def __payload_assembler_(self):
        documents_list = []
        url_list = []
        index = 0
        for content_with_url in itertools.islice(self.content_gen, self.MAX_CONCURRENT_CONTENT):
            index +=1

            document = {
                "id": str(index),
                "language": "en",
                "text": content_with_url[0]
            }
            documents_list.append(document)
            url_list.append(content_with_url[1])

        payload = { "documents" : documents_list }

        fake_list = ["1", "2" ,"3", "4"]
        return payload, fake_list

    def __azure_text_analysis_(self, payload):
        languague_api_url = self.AZURE_ENDPOINT + "/text/analytics/v3.0-preview.1/keyPhrases"
        headers = {"Ocp-Apim-Subscription-Key": self.AZURE_SUBSCRIPTION_KEY}
        # response = requests.post(languague_api_url, headers=headers, json=payload)
        # key_phrases = response.json()

        fake_return = {
            "documents":[
                {
                "keyPhrases":[
                    "wonderful experience",
                    "staff",
                    "rooms"
                ],
                "id":"1"
                },
                {
                "keyPhrases":[
                    "food",
                    "terrible time",
                    "hotel",
                    "staff"
                ],
                "id":"2"
                },
                {
                "keyPhrases":[
                    "Monte Rainier",
                    "caminos"
                ],
                "id":"3"
                },
                {
                "keyPhrases":[
                    "carretera",
                    "tráfico",
                    "día"
                ],
                "id":"4"
                }
            ],
            "errors":[]
            }

        return fake_return

    def _tag_scraper_(self):
        for _ in self.content_gen:
            assembler_output = self.__payload_assembler_()

            azure_response = self.__azure_text_analysis_(assembler_output[0])
            key_phrases_list = azure_response['documents']

            mongo_package = []
            for key_phrase_json in key_phrases_list:
                mongo_document_update = {
                    "url": assembler_output[1][key_phrases_list.index(key_phrase_json)],
                    "tags_raw": key_phrase_json['keyPhrases'],
                    "tagged": True
                }
                mongo_package.append(mongo_document_update)
        print(mongo_package)



if __name__ == "__main__":
    ts = __TagScraper__()
    ts._tag_scraper_()
    #ts._content_manager_()
    # content_generator = ts._get_content_()
    # for article in content_generator:
    #     print(len(article))

