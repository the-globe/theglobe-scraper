xpath_selectors = {
    'name' : ['//meta[@property="og:site_name"]/@content'],
    'publishedAt' : [
        '//meta[@name="article.published"]/@content',
        '//meta[@itemprop="datePublished"]/@content',
    ],
    'modifiedAt' : [
        '//meta[@name="article.updated"]/@content',
        '//meta[@itemprop="dateModified"]/@content',
    ],
    'title' : [
        '//h1/text()',
        '//meta[@property="og:title"]/@content',
    ],
    'title_detail' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content'
    ],
    'urlToImg' : [
        '//meta[@property="og:image"]/@content'
    ],
    'author' : [
        '//meta[@name="author"]/@content',
        '//meta[@property="article:author"]/@content',
    ],
    # 'content' : [
    #     '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    # ],
    'section' : [
        '//meta[@property="og:section"]/@content',
    ],
    'tags': [
        '//meta[@name="news_keywords"]/@content', # not a list
        '//meta[@name="keywords"]/@content', # not a list
    ],
    'type': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': False, # True if many schemas are in a list
    'list_index': None, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}