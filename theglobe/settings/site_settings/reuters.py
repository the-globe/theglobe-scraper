xpath_selectors = {
    'name' : ['//meta[@property="og:site_name"]/@content'],
    'publishedAt' : [
        '//meta[@property="og:pubdate"]/@content',
        '//meta[@property="article:published_time"]/@content',
        '//meta[@name="pubdate"]/@content',
    ],
    'modifiedAt' : [
        '//meta[contains(@property, "article:modified_time")]/@content',
        '//meta[@name="lastmod"]/@content',
    ],
    'title' : [
        '//h1/text()',
        '//meta[@property="og:title"]/@content',
    ],
    'title_detail' : [
        '//meta[@property="og:description"]/@content',
        '//meta[@name="description"]/@content'
    ],
    'url' : [
        '//link[@rel="canonical"]/@href'
    ],
    'urlToImg' : [
        '//meta[@property="og:image"]/@content'
    ],
    'author' : [
        '//meta[@name="author"]/@content',
        '//meta[@property="og:author"]/@content'
    ],
    # 'content' : [
    #     '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    # ],
    'section' : [
        '//meta[@property="og:article:section"]/@content',
    ],
    'tags': [
        '//meta[@name="keywords"]/@content',
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