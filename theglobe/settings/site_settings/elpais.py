selectors = {
    'NAME_SELECTORS' : ['//meta[@property="og:site_name"]/@content'],
    'PUB_DATE_SELECTORS' : [
        '//meta[@property="article:published_time"]/@content',
    ],
    'MOD_DATE_SELECTORS' : [
        '//meta[@property="article:modified_time"]/@content',
        '//meta[@property="og:updated_time"]/@content',
    ],
    'TITLE_SELECTORS' : [
        '//h1/text()',
        '//meta[@property="og:title"]/@content',
    ],
    'TITLE_DETAIL_SELECTORS' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content',
    ],
    'IMAGE_SELECTORS' : [
        '//meta[@property="og:image"]/@content',
    ],
    'AUTHOR_SELECTORS' : [
        '//meta[@name="author"]/@content',
        '//meta[@property="og:article:author"]/@content',
        '//meta[@itemprop="author"]/@content',
    ],
    'CONTENT_SELECTORS' : [
        '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    ],
    'SECTION_SELECTORS' : [
        '//meta[@property="article:section"]/@content',
    ],
    'TAG_SELECTORS': [
        '//meta[@property="article:tag"]/@content',
        '//meta[@name="news_keywords"]/@content',
        '//meta[@name="keywords"]/@content',
    ],
    'TYPE_SELECTORS': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': True, # True if many schemas are in a list
    'list_index': 2, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}