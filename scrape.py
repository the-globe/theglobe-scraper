# python scrape.py -s <arg>
# When passing 'test' as 'arg' redis and mongodb will be disabled
# When passing 'debug' as 'arg' debug will be set in logging

import logging
import theglobe
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys, getopt
import os




def main(s):
    process = CrawlerProcess(s)
    process.crawl(theglobe.ArticlesSpider)
    process.start()


def check_args(argv):
    help_msg = ('scrape.py -s <settingtype> -l <loglevel>\n\t-s "test"\n\t-l "debug"\n\t-h for help')
    try:
        opts, args = getopt.getopt(argv,"hs:l:u:",["settings=", "logging=","urls="])
    except getopt.GetoptError:
            print(help_msg)
            sys.exit(2)
    s = get_project_settings()
    for opt, arg in opts:
        if opt == '-h':
            print(help_msg)
            sys.exit()
        elif opt in ("-s", "--settings"):
            setting_type = arg
            cs = change_settings(s, setting_type)
            if cs:
                s = cs
                print(f"Using '{arg}' settings!")
            else:
                print(f"'{arg}' is not a valid arg!")
                sys.exit(2)
        elif opt in ("-l", "--logging"):
            logging_level = arg
            cs = change_logging_level(s, logging_level)
            if cs:
                print(f"Logging level = {cs['LOG__LEVEL']}")
                s = cs
            else:
                print(f"'{arg}' is not a valid arg!")
                sys.exit(2)
    return s


def change_logging_level(s, level):
    print(level)
    if level == 'debug':
        s['LOG__LEVEL'] = "DEBUG"
        return s
    else:
        return False


def change_settings(s, s_type):
    if s_type == 'test':
        s['TESTING'] = True
        s['ITEM_PIPELINES'] = {
    'theglobe.pipelines.TheglobePipeline': 350,
    'theglobe.pipelines.JsonWriterPipeline': 500,
        }
    else:
        return False
    return s


if __name__ == "__main__":
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'theglobe.settings.global'
    try:
        s = check_args(sys.argv[1:])
        if s == None:
            s = get_project_settings()
        # This has to be on top level!
        theglobe.InitLogging(s['LOG__LEVEL'])
        logger = logging.getLogger(__name__)

        main(s)

    except Exception:
        logger.error('An Error araised', exc_info=True)