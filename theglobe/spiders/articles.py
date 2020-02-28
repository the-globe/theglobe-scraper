# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import logging
import datetime

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

        article = self._get_schema_content_(response)

        article = {
            'name': self._get_name_(response),
            'title': self._get_title_(response),
            'title_detail': self._get_title_detail_(response),
            'author': self._get_author_(response),
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

    def _get_schema_content_(self, response):
        SCHEMA_SELECTORS = self.settings.getlist('SCHEMA_SELECTORS')
        for item in SCHEMA_SELECTORS:
            try:
                schema = response.xpath(item).get()
            except Exception:
                continue
            else:
                self.logger.critical(f"SCHEMA: {schema}")
                return schema
        self.logger.critical(f"None of the given selectors worked for: {response.url} ")
        return("N/A")

    def _get_name_(self, response):
        """Get the name of the Newspaper."""
        NAME_SELECTORS = self.settings.getlist('NAME_SELECTORS')
        for item in NAME_SELECTORS:
            try:
                name = response.xpath(item).get()
            except Exception:
                continue
            else:
                return name
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_title_(self, response):
        """Get the title of the article."""
        TITLE_SELECTORS = self.settings.getlist('TITLE_SELECTORS')
        for item in TITLE_SELECTORS:
            try:
                title = response.xpath(item).get()
            except Exception:
                continue
            else:
                return title
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_title_detail_(self, response):
        """
        Get a detailed title of the article.
        Mostly called "description".
        """
        TITLE_DETAIL_SELECTORS = self.settings.getlist('TITLE_DETAIL_SELECTORS')
        for item in TITLE_DETAIL_SELECTORS:
            try:
                title_detail = response.xpath(item).get()
            except Exception:
                continue
            else:
                return title_detail
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")

    def _get_author_(self, response):
        """
        Get the author of the article.
        This can sometimes be a bit tricky:
        BBC only has itself as author of the article.
        """
        AUTHOR_SELECTORS = self.settings.getlist('AUTHOR_SELECTORS')
        for item in AUTHOR_SELECTORS:
            try:
                author = response.xpath(item).get()
            except Exception:
                continue
            else:
                return author
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")

    def _get_summary_(self, response):
        """
        Get a summary of the article.
        Sometimes the articles only have a title and description, but no summary.
        """
        SUMMARY_SELECTORS = self.settings.getlist('SUMMARY_SELECTORS')
        for item in SUMMARY_SELECTORS:
            try:
                summary = response.xpath(item).get()
            except Exception:
                continue
            else:
                return summary
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_content_(self, response):
        """
        Get the whole content of the article.
        TODO This is still pretty hard to do
        regarding to the fact that there are many different article types.
        """
        CONTENT_SELECTORS = self.settings.getlist('CONTENT_SELECTORS')
        for item in CONTENT_SELECTORS:
            try:
                content = response.xpath(item).get()
            except Exception:
                continue
            else:
                return content
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_tags_(self, response):
        """
        Get the keywords/tags.
        Some websites have keyword/tags regardning to the articles topic.
        """
        KEYWORD_SELECTORS = self.settings.getlist('KEYWORD_SELECTORS')
        for item in KEYWORD_SELECTORS:
            try:
                keywords = response.xpath(item).get()
            except Exception:
                continue
            else:
                return keywords
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_urlToImg_(self, response):
        """
        Get the main Image of the article. 
        Articles can have more than one picture,
        but this method only wants to get the main picture.
        """
        IMAGE_SELECTORS = self.settings.getlist('IMAGE_SELECTORS')
        for item in IMAGE_SELECTORS:
            try:
                url_to_img = response.xpath(item).get()
            except Exception:
                continue
            else:
                return url_to_img
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")


    def _get_publishedAt_(self, response):
        """
        Get the published date of the article.
        Articles can have many different date data.
        Most important, though, is when the article got published. 
        """
        PUB_DATE_SELECTORS = self.settings.getlist('PUB_DATE_SELECTORS')
        DATE_FORMATS = self.settings.getlist('DATE_FORMATS')

        """
        TODO BBC doesn't provide specific data in the meta tags
        they are working with schema.org though.
        e.g. : <script type="application/ld+json"> {key:value} </script>
        """

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
        self.logger.debug(f"None of the given Selectors worked for: {response.url}")
        return("N/A")
