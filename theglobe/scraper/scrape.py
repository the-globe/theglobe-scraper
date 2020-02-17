# scraper/scrape.py

import feedparser
import datetime
from html.parser import HTMLParser
import logging

class Scrape():
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.logger.info("Scraper initialized")


    def _img_finder_(self):
        """TODO: use HTML parser to get img tag and href attribute"""
        pass


    def _get_articles_(self, url_list):
        articles_json_list = {'articles':[]}
        for url in url_list:
            parsed_newspaper = self._rss_feed_parser_(url)
            if type(parsed_newspaper) == list:
                articles_json_list['articles'].extend(parsed_newspaper)
            else:
                self.logger.error(f"Paper{url} returned error: " + parsed_newspaper)   
        self.logger.debug(f"News in total found: {len(articles_json_list['articles'])}")
        return articles_json_list


    def _rss_feed_parser_(self, url):

        newsfeed = feedparser.parse(url)
        news = newsfeed.entries

        """ If paper has no name return as error and skip """
        try:
            paper_name = newsfeed.feed.title
        except Exception:
            self.logger.error(f"An Error araised", exc_info=True)
        
        self.logger.debug(f'Number of posts in {paper_name}: {str(len(newsfeed.entries))}')

        post_json_list = []

        for post in news:
            """ Tries to add an author """
            try:
                post_author = post.author
            except AttributeError:
                post_author = "N/A"

            """ Tries to get post summary """
            try:
                post_summary = post.summary
            except AttributeError:
                post_summary = "N/A"

            """ Tries to get content """
            try:
                """ TODO fix 'seguir leyendo' """
                post_content = post.content[0]["value"]
            except AttributeError:
                """ TODO GET CONTENT MANUALLY THROUGH HTML PARSE """
                post_content = "N/A"

            """ Tries to get post image """
            try:
                post_img = post.links[1]["href"]
            except (AttributeError, IndexError):
                """ TODO use __img_finder get image manually """
                post_img = "N/A"

            """ Extracts post url from object in list """
            post_url = post.links[0]["href"]

            """ Universalize time """
            try:
                time_posted = datetime.datetime(post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday, post.published_parsed.tm_hour, post.published_parsed.tm_min, post.published_parsed.tm_sec)
            except AttributeError:
                try:
                    time_posted = post.published
                except AttributeError:
                    time_posted = "N/A"

            time_added = datetime.datetime.now()

            post_json = {
                "name": paper_name,
                "author": post_author,
                "title": post.title,
                "title_detail": post.title_detail.value,
                "summary": post_summary,
                "content": post_content,
                "tags": "placeholder",
                "url": post_url,
                "urlToImg": post_img,
                "publishedAt": time_posted,
                "addedAt": time_added,
                "score": "placeholder"
            }

            post_json_list.append(post_json)

        return post_json_list

"""
TODO:
    parse html of article and get text
    create system that detects tags
    write bot that looks for img in article
"""