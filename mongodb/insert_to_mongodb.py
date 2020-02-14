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
    """Get articles"""
    scraped_articles = {'articles':[]}
    for newspaper in ['http://feeds.bbci.co.uk/news/england/london/rss.xml', 'https://www.spiegel.de/international/index.rss', 'https://elpais.com/rss/elpais/inenglish.xml', 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'http://rss.cnn.com/rss/edition.rss', 'http://rss.cnn.com/rss/cnn_topstories.rss', 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories', 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms', 'https://feeds.a.dj.com/rss/RSSWorldNews.xml', 'https://www.rt.com/rss/news/', 'https://www.latimes.com/world/rss2.0.xml', 'https://www.buzzfeed.com/world.xml', 'http://www.aljazeera.com/xml/rss/all.xml', 'https://www.cbc.ca/cmlink/rss-world', 'http://www.independent.co.uk/news/world/rss', 'http://feeds.reuters.com/Reuters/worldNews']:

        scraped_articles['articles'].append(parser(newspaper)[0])
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
        print("\nInserted ID's: ", result.inserted_ids, "\n")
        return result


if __name__ == '__main__':
    """Initialize Database"""
    client, db, collection = initilize_db(URL, DB, COLLECTION)

    """Get the articles"""
    scraped_articles = get_articles()

    """Check the Date of the articles"""
    checked_articles = check_date(scraped_articles)

    """Insert the articles and get the result (Mongo id's)"""
    result = insert_articles(collection, checked_articles)

    serverStatusResult = db.command("serverStatus")
    pprint(serverStatusResult)
