# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import json
import logging
import datetime
from .data_handling import DataHandler

class ArticlesSpider(scrapy.Spider):
    """Spider to scrape articles from news websites."""

    name = 'articles'

    def __init__(self, urls, *args, **kwargs):
        super(ArticlesSpider, self).__init__(*args, **kwargs)
        if not urls:
            self.logger.error("No urls passed!")
        self.urls = urls


    def start_requests(self):
        """Start a request for each url that got passed."""
        for url in self.urls:
            yield scrapy.Request(url, self._check_url_)


    def _check_url_(self, response):
        """ TODO Load shema for different news websites """

        SET_SELECTOR = '//channel/item'
        for article in response.xpath(SET_SELECTOR):
            CONTENT_LINK = './/link/text()'

            article_url = article.xpath(CONTENT_LINK).extract_first()

            """ TODO check if url exist in redis
            if check == False:
                pass
            else:
                add to redis
                make the request below
            """
            yield scrapy.Request(article_url, self._parse_)

    def _parse_(self, response):
        """ TODO Get all data -> summary, author, content, tags"""
        self.logger.debug('A response from %s just arrived!', response.url)

        self.data_handler = DataHandler(response, self.settings)

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