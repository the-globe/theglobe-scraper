import logging
import theglobe
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings




def main(urls):
    process = CrawlerProcess(get_project_settings())
    """ TODO multi-threading """
    process.crawl(theglobe.ArticlesSpider, urls = list(urls))
    process.start()


if __name__ == "__main__":
    try:
        # This has to be on top level!
        theglobe.InitLogging()
        logger = logging.getLogger(__name__)

        main(["http://rss.cnn.com/rss/edition.rss", "http://feeds.bbci.co.uk/news/rss.xml"])
        
    except Exception:
        logger.error('An Error araised', exc_info=True)