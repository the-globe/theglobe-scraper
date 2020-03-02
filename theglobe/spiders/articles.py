# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json
import logging
import datetime
from theglobe.data_handler import DataHandler
import theglobe.redis


class ArticlesSpider(scrapy.Spider):
    """Spider to scrape articles from news websites."""

    name = 'article_scraper'

    def __init__(self, stats, settings):
        super(ArticlesSpider, self).__init__()
        self.stats = stats
        self.settings = settings
        self.rm = theglobe.redis.RedisManager(settings, stats)
        """Get URL's from database"""
        self.urls = [
            "http://rss.cnn.com/rss/edition.rss",
            # "http://feeds.bbci.co.uk/news/rss.xml"
            ]


    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            stats = crawler.stats,
            settings = crawler.settings
        )


    def start_requests(self):
        """Start a request for each url that got passed."""        
        if not self.urls:
            self.logger.error("No urls passed!")

        for url in self.urls:
            yield scrapy.Request(url, self._check_url_)


    def _check_url_(self, response):
        """ TODO Load shema for different news websites """

        SET_SELECTOR = '//channel/item'
        for article in response.xpath(SET_SELECTOR):
            CONTENT_LINK = './/link/text()'

            article_url = article.xpath(CONTENT_LINK).extract_first()

            if self.rm._bf_check_url_pres_(article_url):
                pass
            else:
                self.rm._bf_add_url_(article_url)
                yield scrapy.Request(article_url, self._parse_)

    def _parse_(self, response):
        """ TODO Get all data -> summary, author, content, tags"""
        self.logger.debug('A response from %s just arrived!', response.url)

        self.data_handler = DataHandler(response, self.settings, self.stats)

        article = self.data_handler._get_all_data_()

        if article:
            article['addedAt'] = datetime.datetime.utcnow()
            article['score'] = "N/A"
            article['url'] = response.url

            self.logger.debug(article)
            yield article

        else:
            self.logger.error("No data in article document")
            self.logger.info(article)