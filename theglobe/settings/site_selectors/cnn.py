dict = {
    'NAME_SELECTORS' : ['//meta[@property="og:site_name"]/@content'],
    'PUB_DATE_SELECTORS' : [
        '//meta[@property="og:pubdate"]/@content',
        '//meta[@property="article:published_time"]/@content',
        '//meta[@name="pubdate"]/@content',
    ],
    'MOD_DATE_SELECTORS' : [
        '//meta[contains(@property, "article:modified_time")]/@content',
        '//meta[@name="lastmod"]/@content',
    ],
    'TITLE_SELECTORS' : ['//h1/text()'],
    'TITLE_DETAIL_SELECTORS' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content'
    ],
    'IMAGE_SELECTORS' : [
        '//meta[@property="og:image"]/@content'
    ],
    'AUTHOR_SELECTORS' : [
        '//meta[@name="author"]/@content',
        '//meta[@property="og:author]/@content'
    ],
    'CONTENT_SELECTORS' : [
        '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    ],
    'TAG_SELECTORS': [
        '//meta[@name="section"]/@content',
    ],
}

def get(name):
    return dict[name]