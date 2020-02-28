NAME_SELECTORS = ['//meta[@property="og:site_name"]/@content']
PUB_DATE_SELECTORS = [
    '//meta[contains(@name, "pub")]/@content',
    '//meta[contains(@name, "Pub")]/@content',
    '//meta[contains(@property, "Pub")]/@content',
    '//meta[contains(@property, "pub")]/@content',
    '//meta[@property="og:pubdate"]/@content',
    '//meta[@name="pubdate"]/@content',
    '//meta[@itemprop="datePublished"]/@content'
]
MOD_DATE_SELECTORS = [
    '//meta[contains(@itemprop, "dateModified")]/@content',
    '//meta[contains(@name, "mod")]/@content',
    '//meta[contains(@property, "mod")]/@content'
    '//meta[contains(@name, "Mod")]/@content',
    '//meta[contains(@property, "Mod")]/@content'
]
DATE_FORMATS = [
    '%Y-%m-%dT%H:%M:%S.%fZ',
    '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S+00:00',
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S'
]
TITLE_SELECTORS = ['//h1/text()']
TITLE_DETAIL_SELECTORS = ['//meta[@property="og:description"]/@content']
IMAGE_SELECTORS = ['//meta[@property="og:image"]/@content']
AUTHOR_SELECTORS = ['//meta[@name="author"]/@content']
SCHEMA_SELECTORS = ['//script[@type="application/ld+json"]/text()']