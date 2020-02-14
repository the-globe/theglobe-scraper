import feedparser
import datetime
from html.parser import HTMLParser

url_list = ['http://feeds.bbci.co.uk/news/england/london/rss.xml', 'https://www.spiegel.de/international/index.rss', 'https://elpais.com/rss/elpais/inenglish.xml', 'https://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'http://rss.cnn.com/rss/edition.rss', 'http://rss.cnn.com/rss/cnn_topstories.rss', 'http://rssfeeds.usatoday.com/usatoday-NewsTopStories', 'https://timesofindia.indiatimes.com/rssfeeds/296589292.cms', 'https://feeds.a.dj.com/rss/RSSWorldNews.xml', 'https://www.rt.com/rss/news/', 'https://www.latimes.com/world/rss2.0.xml', 'https://www.buzzfeed.com/world.xml', 'http://www.aljazeera.com/xml/rss/all.xml', 'https://www.cbc.ca/cmlink/rss-world', 'http://www.independent.co.uk/news/world/rss', 'http://feeds.reuters.com/Reuters/worldNews']

def __img_finder():
    pass

def rss_feed_parser(feed_url):

    newsfeed = feedparser.parse(feed_url)
    news = newsfeed.entries

    print('Number of posts: ' + str(len(newsfeed.entries)))

    #post = news[1]

    # print(post.keys())
    # print(post.links)

    post_json_list = []

    for post in news: 
        # Tries to add an author
        try:
            post_author = post.author
        except AttributeError:
            post_author = "N/A"

        # Tries to get content
        try:
            #TODO: fix seguir leyendo
            post_content = post.content[0]["value"]
        except AttributeError:
            # TODO GET CONTENT MANUALLY THROUGH HTML PARSE
            post_content = "N/A"

        # Tries to get post image
        try:
            post_img = post.links[1]["href"]
        except AttributeError:
            #TODO get image manually
            post_img = "N/A"

        # Extracts post url from object in list
        post_url = post.links[0]["href"]

        # Universalize time
        time_posted = datetime.datetime(post.published_parsed.tm_year, post.published_parsed.tm_mon, post.published_parsed.tm_mday, post.published_parsed.tm_hour, post.published_parsed.tm_min, post.published_parsed.tm_sec)
        time_added = datetime.datetime.now()

        post_json = {
            "name": newsfeed.feed.title,
            "author": post_author,
            "title": post.title,
            "title_detail": post.title_detail.value,
            "summary": post.summary,
            "content": post_content,
            "tags": "placeholder",
            "url": post_url,
            "urlToImg": post_img,
            "publishedAt": time_posted,
            "addedAt": time_added,
            "score": "placeholder"
        }


        #print(post_json)

        post_json_list.append(post_json)

    return post_json_list

# TODO:
# parse html of article and get text
# create system that detects tags
# write bot that looks for img in article