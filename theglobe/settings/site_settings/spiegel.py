xpath_selectors = {
    'name' : [
    ],
    'publishedAt' : [
        '//meta[@name="date"]/@content'
    ],
    'modifiedAt' : [
        '//meta[@name="last-modified"]/@content'
    ],
    'title' : [
        '//h1/text()',
        '//meta[@property="og:title"]/@content',
    ],
    'title_detail' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content',
    ],
    'urlToImg' : [
        '//meta[@property="og:image"]/@content',
    ],
    'author' : [
        '//meta[@name="author"]/@content',
    ],
    # 'content' : [
    #     '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    # ],
    'section' : [
    ],
    'tags': [
        '//meta[@name="news_keywords"]/@content',
    ],
    'type': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': True, # True if many schemas are in a list
    'list_index': 0, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}