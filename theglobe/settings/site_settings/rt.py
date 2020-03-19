selectors = {
    'NAME_SELECTORS' : ['//meta[@property="og:site_name"]/@content'],
    'PUB_DATE_SELECTORS' : [
    ],
    'MOD_DATE_SELECTORS' : [
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
        '//meta[@name="article:author"]/@content',
    ],
    'CONTENT_SELECTORS' : [
        '//div[@itemprop = "articleBody"]/descendant::text()[not(ancestor::script)]',
    ],
    'SECTION_SELECTORS' : [
        '//meta[@name="article:section"]/@content',
    ],
    'TAG_SELECTORS': [
        # has no tags / keywords
    ],
    'TYPE_SELECTORS': [
        '//meta[@property="og:type"]/@content',
    ],
}

schema_handling = {
    'index': 2, # what script should we looked at
    'list_check': False, # True if many schemas are in a list
    'list_index': None, # if it's a list this should be an int()
    'fixed_type': 'NEWSARTICLE', # accepted type
}