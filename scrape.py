# python scrape.py -s <arg>
# When passing 'test' as 'arg' redis and mongodb will be disabled

import logging
import theglobe
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys, getopt




def main(s):
    process = CrawlerProcess(s)
    process.crawl(theglobe.ArticlesSpider)
    process.start()


def check_args(argv):
    try:
        opts, args = getopt.getopt(argv,"hs:",["settings="])
    except getopt.GetoptError:
            print('test.py -s <settingtype> e.g. test')
            sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -s <settingtype> e.g. test')
            sys.exit()
        elif opt in ("-s", "--settings"):
            setting_type = arg
            s = change_settings(setting_type)
            if s:
                print(f"Using '{arg}' settings!")
                return s
            else:
                print(f"'{arg}' is not a valid arg!")
                sys.exit(2)


def change_settings(type):
    s = get_project_settings()
    if type == 'test':
        s['TESTING'] = True
        s['ITEM_PIPELINES'] = {
    'theglobe.pipelines.TheglobePipeline': 350,
    'theglobe.pipelines.JsonWriterPipeline': 500,
        }
        return s
    else:
        return s


if __name__ == "__main__":
    try:
        s = check_args(sys.argv[1:])
        if s == None:
            s = get_project_settings()
        # This has to be on top level!
        theglobe.InitLogging()
        logger = logging.getLogger(__name__)

        main(s)

    except Exception:
        logger.error('An Error araised', exc_info=True)