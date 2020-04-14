xpath_selectors = {
    'name' : ['//meta[@property="og:site_name"]/@content'],
    'publishedAt' : [
        '//meta[@property="rnews:datePublished"]/@content',
        '//meta[contains(@property, "datePublished")]/@content',
    ],
    'modifiedAt' : [
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
        # '//meta[@property="article:author"]/@content' # this will return an url to bbc's facebook
    ],
    # 'content' : [
    #    '//div[contains(@class, "story-body__inner")]/*[not(self::figure)]',
    #    '//div[contains(@property, "articleBody")]/*[not(self::figure)]'
    #    '//div[contains(@itemprop, "articleBody")]',
    #]
    'section': [
        '//meta[@property="article:section"]/@content',
        '//meta[@name="section"]/@content',
    ],
    'tags': [
    ],
    'type': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 0, # what script should we looked at
    'list_check': False, # True if many schemas are in a list
    'list_index': None, # if it's a list this should be an int()
    'fixed_type': None, # accepted type
}