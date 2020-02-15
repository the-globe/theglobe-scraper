from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from pymongo import WriteConcern
from pprint import pprint

import logging
import os
import json
import logging.config

from datetime import datetime

from rss_feed_parser import rss_feed_parser as parser


USERNAME = "crawlerMarvin"
PASSWORD = "mDN57nBndxoX8TAJ"
URL = ("mongodb://b.lnru.de:27017/")
DB = "tg"
COLLECTION = "articles"
URL_LIST = [
            'http://feeds.bbci.co.uk/news/england/london/rss.xml', 
            'https://www.spiegel.de/international/index.rss', 
            'https://elpais.com/rss/elpais/inenglish.xml', 
            'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 
            'http://rss.cnn.com/rss/edition.rss', 
            'http://rss.cnn.com/rss/cnn_topstories.rss', 
            'http://rssfeeds.usatoday.com/usatoday-NewsTopStories', 
            'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms', 
            'https://feeds.a.dj.com/rss/RSSWorldNews.xml', 
            'https://www.rt.com/rss/news/', 
            'https://www.latimes.com/world/rss2.0.xml', 
            'http://www.aljazeera.com/xml/rss/all.xml', 
            'https://www.cbc.ca/cmlink/rss-world', 
            'http://www.independent.co.uk/news/world/rss', 
            'http://feeds.reuters.com/Reuters/worldNews']

def initilize_db(URL, DB, COLLECTION):
    try:
        client = MongoClient(URL)
        db = client[DB]
        collection = db[COLLECTION]
    except Exception as err:
        print(type(err))
        print('An error accured: ', err)
    else:
        return client, db, collection


def get_articles(URL_LIST):
    """
    Take articles from Scraper Class
    return scraped_articles
    """
    """Get articles"""
    scraped_articles = {'articles':[]}
    for newspaper in URL_LIST:
        parsed_newspaper = parser(newspaper)
        if type(parsed_newspaper) == list:
            scraped_articles['articles'].extend(parsed_newspaper)
        else:
            print(f"Paper{newspaper} returned error: " + parsed_newspaper)
    print(f"\nNews in total found: {len(scraped_articles['articles'])}")
    return(scraped_articles)


def check_date(scraped_articles):
    """Not clear, yet"""
    # for article in scraped_articles['articles']:
    #     if type(article['publishedAt']) != datetime or type(article['addedAt']) != datetime:
    #         article['publishedAt'] = datetime.strptime(article['publishedAt'], '%Y-%m-%d %H:%M:%S')
    #         article['addedAt'] = datetime.strptime(article['addedAt'], '%Y-%m-%d %H:%M:%S')
    #     else:
    #         print("Formatting of the dates is fine!")
    return scraped_articles


def insert_articles(collection, checked_articles):
    """Insert Articles to the assigned Collection"""
    try:
        # w_0 = collection.with_options(write_concern=WriteConcern(w=0))
        basic_logger.info(f"Try to insert {len(checked_articles['articles'])} articles.")
        r = collection.insert_many(checked_articles['articles'], ordered = False)
    except BulkWriteError as bwe:
        insert_logger.debug(f"Insert error accured: {bwe} {type(bwe)}")

        list_failed_inserts = []
        for item in bwe.details['writeErrors']:
            item = [item['index'],item['op']['_id']]
            list_failed_inserts.append(item)
        insert_logger.debug(f"{list_failed_inserts}")

        list_of_details = []
        for item in ['writeConcernErrors', 'nInserted', 'nUpserted', 'nMatched', 'nModified', 'nRemoved', 'upserted']:
            list_of_details.append(f"{item}:{bwe.details[item]}")
        insert_logger.debug(f"{list_of_details}")

        basic_logger.info(f"Inserted documents: {bwe.details['nInserted']}")
        basic_logger.info(f"Failed documents: {len(checked_articles['articles']) - bwe.details['nInserted']}")
    else:
        basic_logger.info(f"Inserted documents: {len(r.inserted_ids)}")


def setup_logging(default_path='logging.json', default_level=logging.INFO, env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    # value = os.getenv(env_key, None)
    # if value:
    #     path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)   


if __name__ == '__main__':

    setup_logging()

    basic_logger = logging.getLogger("basic_logger")
    err_logger = logging.getLogger('error_logger')
    insert_logger = logging.getLogger('failed_insert_logger')

    basic_logger.info(f'Crawler Started!')

    # Initialize Database
    client, db, collection = initilize_db(URL, DB, COLLECTION)

    # Get the articles
    scraped_articles = get_articles(URL_LIST)

    # Check the Date of the articles
    checked_articles = check_date(scraped_articles)

    # Insert the articles and get the result (Mongo id's)
    insert_articles(collection, checked_articles)

    # serverStatusResult = db.command("serverStatus")
    #pprint(serverStatusResult)

    basic_logger.info(f'Crawler Terminated!')
