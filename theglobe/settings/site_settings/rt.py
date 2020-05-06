xpath_selectors = {
    'name' : ['//meta[@property="og:site_name"]/@content'],
    'publishedAt' : [
    ],
    'modifiedAt' : [
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
        '//meta[@name="article:author"]/@content',
    ],
    # 'content' : [
    #     '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    # ],
    'section' : [
        '//meta[@name="article:section"]/@content',
    ],
    'tags': [
        # has no tags / keywords
    ],
    'type': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 2, # what script should we looked at
    'list_check': False, # True if many schemas are in a list
    'list_index': None, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}