from .schemas import *

# -*- coding: utf-8 -*-

# Scrapy settings for theglobe project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'theglobe'

SPIDER_MODULES = ['theglobe.spiders']
NEWSPIDER_MODULE = 'theglobe.spiders'

LOG_ENABLED = False

LOG__LEVEL = 'INFO' # Attention! This is not the usual LOG_LEVEL variable for scrapy

# MongoDB Settings
MONGO_URL = 'mongodb://rdwc.de:27017/'
MONGO_DATABASE = 'tg'
MONGO_COLLECTION = 'articles-testing'

# Redis Server Settings
REDIS_ENABLED = False #boolean
REDIS_HOST = "rdwc.de"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

TESTING = False

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'theglobe (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'theglobe.middlewares.TheglobeSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'theglobe.middlewares.TheglobeDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'theglobe.pipelines.TheglobePipeline': 350,
   'theglobe.pipelines.JsonWriterPipeline': 500,
   'theglobe.pipelines.MongoPipeline': 800,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Settings for articles spider

# The Schema selector is always the same
SCHEMA_ORG_SELECTOR = '//script[@type="application/ld+json"]/text()'

# This is the default dictionary of selectors to handle the websites -> default = []
DEFAULT_SELECTORS = {
    'name': {
        'schema_org': [],
        'xpath': [],
    },
    'title': {
        'schema_org': [],
        'xpath': [],
    },
    'title_detail': {
        'schema_org': [],
        'xpath': [],
    },
    'author': {
        'schema_org': [],
        'xpath': [],
    },
   #  'content': {
      #   'schema_org': [],
      #   'xpath': [],
   #  },
    'url': {
        'schema_org': [],
        'xpath': [],
    },
    'urlToImg': {
        'schema_org': [],
        'xpath': [],
    },
    'publishedAt': {
        'schema_org': [],
        'xpath': [],
    },
    'modifiedAt': {
        'schema_org': [],
        'xpath': [],
    },
    'type': {
        'schema_org': [],
        'xpath': [],
    },
    'tags': {
        'schema_org': [],
        'xpath': [],
    },
    'section': {
        'schema_org': [],
        'xpath': [],
    }
}
# To get the selector values from above the script needs the key name
XPATH_KEY = 'xpath'
SCHEMA_ORG_KEY = 'schema_org'

# Different schema_org_types (imported from schemas.py)
REPORTAGENEWSARTICLE
BACKGROUNDNEWSARTICLE
WEBPAGE
VIDEOOBJECT
NEWSARTICLE
ANALYSISNEWSARTICLE

# Settings for each news organisation using domain
# Key = domain
# Value = module inside site_settings folder
NEWS_ORGANISATIONS = {
   'edition.cnn.com': 'cnn',
   'www.cnn.com': 'cnn',
   'www.bbc.co.uk': 'bbc',
   'english.elpais.com': 'elpais',
   'elpais.com': 'elpais',
   'timesofindia.indiatimes.com': 'indiatimes',
   'www.rt.com': 'rt',
   'www.latimes.com': 'latimes',
   'www.wsj.com': 'wsj',
   'www.reuters.com': 'reuters',
   'www.spiegel.de' : 'spiegel',
   'www.nytimes.com' : 'nytimes',
   'eu.usatoday.com' : 'usatoday',
   'www.aljazeera.com': 'aljazeera',
   'www.cbc.ca' : 'cbc',
}

# Those are formats to convert string dates to python string type
DATE_FORMATS = [
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%dT%H:%M:%S+00:00',
        '%Y-%m-%d %H:%M:%S',
        '%Y/%m/%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S%z',
        '%Y-%m-%d',
        '%d %b %Y %H:%M %Z',
        '%Y-%m-%dT%H:%MZ',
]

URLS = [
#    'http://feeds.bbci.co.uk/news/england/london/rss.xml',
   'http://feeds.reuters.com/Reuters/worldNews',
#    'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms',
#    'http://rss.cnn.com/rss/edition.rss',
#    'http://rss.cnn.com/rss/cnn_topstories.rss',
#    'https://www.rt.com/rss/news/',
#    'https://www.latimes.com/world/rss2.0.xml',
#    'https://feeds.a.dj.com/rss/RSSWorldNews.xml',
#    'https://elpais.com/rss/elpais/inenglish.xml',
#    'https://www.spiegel.de/international/index.rss',

   # 'http://www.aljazeera.com/xml/rss/all.xml', # TODO needs support for Article schema type
   # 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', # TODO Not able to get the name - Manuel set of name for very site?
   # 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories', # TODO BAD SCHEMA AND META
   # 'https://www.cbc.ca/cmlink/rss-world', # TODO needs configuration from the script, too
   # 'http://www.independent.co.uk/news/world/rss', # TODO not working at all at the moment
]


META_SELECTORS = {
   '@name': '//meta/@name',
   '@property': '//meta/@property',
   '@itemprop': '//div/@itemprop'
}