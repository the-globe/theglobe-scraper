import logging
import theglobe
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings




def main():
    process = CrawlerProcess(get_project_settings())
    process.crawl(theglobe.MetaSpider)
    process.start()


if __name__ == "__main__":
    try:
        # This has to be on top level!
        theglobe.InitLogging()
        logger = logging.getLogger(__name__)

        main()

    except Exception:
        logger.error('An Error araised', exc_info=True)