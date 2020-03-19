# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json
import logging
import datetime
from theglobe.data_handler import DataHandler
import theglobe.redis
from urllib.parse import urlparse


class MetaSpider(scrapy.Spider):
    """Spider to scrape articles from news websites."""

    name = 'meta_scraper'

    def __init__(self, stats, settings, *args, **kwargs):
        super(MetaSpider, self).__init__(*args, **kwargs)
        self.stats = stats
        self.settings = settings
        """Get URL's from database"""
        self.urls = [
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


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        s = cls(
            stats = crawler.stats,
            settings = crawler.settings,
            crawler = crawler
        )
        crawler.signals.connect(s.spider_closed, signal=scrapy.signals.spider_closed)
        return s


    def start_requests(self):
        """Start a request for each url that got passed."""
        if not self.urls:
            self.logger.error("No urls passed!")

        for url in self.urls:
            yield scrapy.Request(url, self._check_url_)


    def _check_url_(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        """ TODO Load shema for different news websites """

        SET_SELECTOR = '//channel/item'
        for article in response.xpath(SET_SELECTOR):
            CONTENT_LINK = './/link/text()'

            article_url = article.xpath(CONTENT_LINK).extract_first()
            yield scrapy.Request(article_url, self._parse_)

    def _parse_(self, response):
        """ TODO Get all data -> summary, author, content, tags"""
        self.logger.debug('A response from %s just arrived!', response.url)
        parsed_uri = urlparse(response.url)
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        self.stats.inc_value(domain)
        list = self.settings.getdict('META_SELECTORS').keys()
        for item in list:
            meta_selector = self.settings.getdict('META_SELECTORS')[item]
            metas = response.xpath(meta_selector).getall()
            for meta in metas:
                self.stats.inc_value(domain+'/'+item+'="'+meta+'"')

    def spider_opened(self, spider):
        print("openeds")

    def spider_closed(self, spider, reason):
        with open('meta.json', 'w') as file:
            json.dump(self.crawler.stats.get_stats(), file, default=str)