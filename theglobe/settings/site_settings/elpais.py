xpath_selectors = {
    'name' : ['//meta[@property="og:site_name"]/@content'],
    'publishedAt' : [
        '//meta[@property="article:published_time"]/@content',
    ],
    'modifiedAt' : [
        '//meta[@property="article:modified_time"]/@content',
        '//meta[@property="og:updated_time"]/@content',
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
        '//meta[@property="og:article:author"]/@content',
        '//meta[@itemprop="author"]/@content',
    ],
    # 'content' : [
    #     '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    # ],
    'section' : [
        '//meta[@property="article:section"]/@content',
    ],
    'tags': [
        '//meta[@property="article:tag"]/@content',
        '//meta[@name="news_keywords"]/@content',
        '//meta[@name="keywords"]/@content',
    ],
    'type': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': True, # True if many schemas are in a list
    'list_index': 2, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}