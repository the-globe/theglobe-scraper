# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import logging
import datetime

class ArticlesSpider(scrapy.Spider):

    name = 'articles'

    def __init__(self, urls, *args, **kwargs):
        super(ArticlesSpider, self).__init__(*args, **kwargs)
        if not urls:
            self.logger.error("No urls passed!")
        self.urls = urls


    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url, self._check_urls_)


    def _check_urls_(self, response):
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
        """ TODO pass all data from article """
        self.logger.debug('A response from %s just arrived!', response.url)

        article = {
            'name': self._get_name_(response),
            'title': self._get_title_(response),
            'title_detail': self._get_title_detail_(response),
            'summary': self._get_summary_(response),
            'content': self._get_content_(response),
            'tags': self._get_tags_(response),
            'urlToImg': self._get_urlToImg_(response),
            'url': response.url,
            'publishedAt': self._get_publishedAt_(response),
            'addedAt': datetime.datetime.utcnow(),
            'score': "N/A"
        }

        yield article


    def _get_name_(self, response):
        NAME_SELECTORS = self.settings.getlist('NAME_SELECTORS')

        for item in NAME_SELECTORS:
            try:
                name = response.xpath(item).get()
            except Exception:
                continue
            else:
                return name
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")

    
    def _get_publishedAt_(self, response):
        PUB_DATE_SELECTORS = self.settings.getlist('PUB_DATE_SELECTORS')
        DATE_FORMATS = self.settings.getlist('DATE_FORMATS')
        for item in PUB_DATE_SELECTORS:
            try:
                response_date = response.xpath(item).get()
                for format in DATE_FORMATS:
                    try:
                        publishedAt = datetime.datetime.strptime(response_date, format)    
                    except Exception:
                        continue
                    else:
                        return publishedAt
            except Exception:
                continue
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_title_(self, response):
        TITLE_SELECTORS = self.settings.getlist('TITLE_SELECTORS')
        for item in TITLE_SELECTORS:
            try:
                title = response.xpath(item).get()
            except Exception:
                continue
            else:
                return title
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_title_detail_(self, response):
        TITLE_DETAIL_SELECTORS = self.settings.getlist('TITLE_DETAIL_SELECTORS')
        for item in TITLE_DETAIL_SELECTORS:
            try:
                title_detail = response.xpath(item).get()
            except Exception:
                continue
            else:
                return title_detail
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_summary_(self, response):
        SUMMARY_SELECTORS = self.settings.getlist('SUMMARY_SELECTORS')
        for item in SUMMARY_SELECTORS:
            try:
                summary = response.xpath(item).get()
            except Exception:
                continue
            else:
                return summary
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_content_(self, response):
        CONTENT_SELECTORS = self.settings.getlist('CONTENT_SELECTORS')
        for item in CONTENT_SELECTORS:
            try:
                content = response.xpath(item).get()
            except Exception:
                continue
            else:
                return content
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_urlToImg_(self, response):
        IMAGE_SELECTORS = self.settings.getlist('IMAGE_SELECTORS')
        for item in IMAGE_SELECTORS:
            try:
                url_to_img = response.xpath(item).get()
            except Exception:
                continue
            else:
                return url_to_img
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")


    def _get_tags_(self, response):
        KEYWORD_SELECTORS = self.settings.getlist('KEYWORD_SELECTORS')
        for item in KEYWORD_SELECTORS:
            try:
                keywords = response.xpath(item).get()
            except Exception:
                continue
            else:
                return keywords
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")

    
    def _get_author_(self, response):
        AUTHOR_SELECTORS = self.settings.getlist('AUTHOR_SELECTORS')
        for item in AUTHOR_SELECTORS:
            try:
                author = response.xpath(item).get()
            except Exception:
                continue
            else:
                return author
        self.logger.debug(f"None of the given Selectors did work for: {response.url}")
        return("N/A")