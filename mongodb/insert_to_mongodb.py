from pymongo import MongoClient

from pprint import pprint

from datetime import datetime

"""Import Santiagos Class / Scraper"""
from rss_feed_parser import rss_feed_parser as parser

USERNAME = "crawlerMarvin"
PASSWORD = "mDN57nBndxoX8TAJ"
URL = ("mongodb://b.lnru.de:27017/")
DB = "tg"
COLLECTION = "articles"

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

def get_articles():
    """
    Take articles from Scraper Class
    return scraped_articles
    """
    try:
        """Get articles"""
        scraped_articles = parser('https://elpais.com/rss/elpais/inenglish.xml')
        # if len(scraped_articles['articles']) == 0:
        #     raise KeyError("There are no articles!")
    except Exception as err:
        print(type(err))
        print('An error accured: ', err)
    else:
        return(scraped_articles)

def check_date(scraped_articles):
    """Not clear, yet"""
    for article in scraped_articles['articles']:
        if type(article['publishedAt']) != datetime or type(article['addedAt']) != datetime:
            article['publishedAt'] = datetime.strptime(article['publishedAt'], '%Y-%m-%d %H:%M:%S')
            article['addedAt'] = datetime.strptime(article['addedAt'], '%Y-%m-%d %H:%M:%S')
        else:
            print("Formatting of the dates is fine!")
    return scraped_articles

def insert_articles(collection, checked_articles):
    """Insert Articles to the assigned Collection"""
    try:
        result = collection.insert_many(checked_articles['articles'])
    except Exception as err:
        print(type(err))
        print('An error accured: ', err)
    else:
        print("\nInserted Id's: ", result.acknowledged, "\n")
        return result


if __name__ == '__main__':
    try:
        """Initialize Database"""
        client, db, collection = initilize_db(URL, DB, COLLECTION)

        """Get the articles"""
        scraped_articles = get_articles()

        """Check the Date of the articles"""
        checked_articles = check_date(scraped_articles)

        """Insert the articles and get the result (Mongo id's)"""
        result = insert_articles(collection, checked_articles)

    except Exception as err:
        print(type(err))
        print('An error accured: ', err)
        print("Script terminated because of an Exception")
    else:
        serverStatusResult = db.command("serverStatus")
        pprint(serverStatusResult)
