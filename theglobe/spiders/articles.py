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

            self.logger.info(article)
            yield article

        else:
            self.logger.error("No data in article document")
            self.logger.info(article)


    # def _get_all_data_(self, response):
    #     schema_content = self._get_schema_content_(response)
    #     if schema_content:
    #         article_schema = self.settings.getdict(schema_content['@type'].upper())
    #         if not article_schema:
    #             self.logger.warning(f"Schema for {schema_content['@type']} doesn't exist")
    #     try:
    #         self.logger.debug(schema_content['@type'])
    #         article = {
    #             'name': self._get_schema_object_(schema_content, article_schema['name']) if article_schema['name'] != None else self._get_name_(response),
    #             'title': self._get_schema_object_(schema_content, article_schema['title']) if article_schema['title'] != None else self._get_title_(response),
    #             'title_detail': self._get_schema_object_(schema_content, article_schema['title_detail']) if article_schema['title_detail'] != None else self._get_title_detail_(response),
    #             'author': self._get_schema_object_(schema_content, article_schema['author']) if article_schema['author'] != None else self._get_author_(response),
    #             'summary': self._get_schema_object_(schema_content, article_schema['summary']) if article_schema['summary'] != None else self._get_summary_(response),
    #             'content': self._get_schema_object_(schema_content, article_schema['content']) if article_schema['content'] != None else self._get_content_(response),
    #             'tags': self._get_schema_object_(schema_content, article_schema['tags']) if article_schema['tags'] != None else self._get_tags_(response),
    #             'urlToImg': self._get_schema_object_(schema_content, article_schema['urlToImg']) if article_schema['urlToImg'] != None else self._get_urlToImg_(response),
    #             'url': response.url,
    #             'publishedAt': self._get_schema_object_(schema_content, article_schema['name']) if article_schema['name'] != None else self._get_publishedAt_(response),
    #             'addedAt': datetime.datetime.utcnow(),
    #             'score': "N/A"
    #         }
    #     except Exception:
    #         self.logger.error(f"Schema:{schema_content['@type']}, URL: {response.url}",exc_info=True)
    #     return article


    # def _get_schema_object_(self, schema_content, x):
    #     try:
    #         if x['range'] == 1:
    #             return schema_content[x['list'][0]]
    #         elif x['range'] == 2:
    #             return schema_content[x['list'][0]][x['list'][1]]
    #         elif x['range'] == 2:
    #             return schema_content[x['list'][0]][x['list'][1]][x['list'][2]]
    #     except Exception:
    #         self.logger.error("Something went wrong with matching Schemas", exc_info=True)
    #         return None