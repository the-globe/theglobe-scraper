selectors = {
    'NAME_SELECTORS' : ['//meta[@property="og:site_name"]/@content'],
    'PUB_DATE_SELECTORS' : [
        '//meta[@name="article.published"]/@content',
        '//meta[@itemprop="datePublished"]/@content',
    ],
    'MOD_DATE_SELECTORS' : [
        '//meta[@name="article.updated"]/@content',
        '//meta[@itemprop="dateModified"]/@content',
    ],
    'TITLE_SELECTORS' : [
        '//h1/text()',
        '//meta[@property="og:title"]/@content',
    ],
    'TITLE_DETAIL_SELECTORS' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content'
    ],
    'IMAGE_SELECTORS' : [
        '//meta[@property="og:image"]/@content'
    ],
    'AUTHOR_SELECTORS' : [
        '//meta[@name="author"]/@content',
        '//meta[@property="article:author"]/@content',
    ],
    'CONTENT_SELECTORS' : [
        '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    ],
    'SECTION_SELECTORS' : [
        '//meta[@property="og:section"]/@content',
    ],
    'TAG_SELECTORS': [
        '//meta[@name="news_keywords"]/@content', # not a list
        '//meta[@name="keywords"]/@content', # not a list
    ],
    'TYPE_SELECTORS': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': False, # True if many schemas are in a list
    'list_index': None, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}