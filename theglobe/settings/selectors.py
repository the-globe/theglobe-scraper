NAME_SELECTORS = ['//meta[@property="og:site_name"]/@content']
PUB_DATE_SELECTORS = [
    '//meta[@property="og:pubdate"]/@content',
    '//meta[@property="article:published_time"]/@content',
    '//meta[@name="pubdate"]/@content',
    '//meta[@itemprop="datePublished"]/@content',
    '//meta[contains(@property, "datePublished")]/@content'
]
MOD_DATE_SELECTORS = [
    '//meta[contains(@itemprop, "dateModified")]/@content',
    '//meta[contains(@property, "article:modified_time")]/@content'
]
DATE_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S+00:00',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%dT%H:%M:%S%z',
    '%Y-%m-%d'

]
TITLE_SELECTORS = ['//h1/text()']
TITLE_DETAIL_SELECTORS = ['//meta[@property="og:description"]/@content']
IMAGE_SELECTORS = ['//meta[@property="og:image"]/@content']
AUTHOR_SELECTORS = ['//meta[@name="author"]/@content']
SCHEMA_SELECTORS = ['//script[@type="application/ld+json"]/text()']