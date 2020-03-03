# Project Structure
```
project/
    scrapy.cfg            # deploy configuration file

    setup.py              # For later deployment

    example.py            # Execution file

    theglobe/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file (insert to mongodb)

        settings/
            __init__.py

            global.py       # project settings file

            selectors.oy    # settings file for all the selectors (article)
            
            schemas.py      # schemas according to schema.org

        spiders/          # a directory with all the spiders
            __init__.py

            articles.py   # This spider Scrapes through news websites to get articles.
            
            data_handling.py # handling the scraped data (sort it)
         
        redis/              # a directory containing the redisbloom manager
            __init__.py
            
            redis_manager.py # manages all bloomfilter requests to the redis server
```

# Project Architecture (Data Flow)
[Google Docs](https://docs.google.com/document/d/1zysHVHg6x2z1DlIxNZfK2KpFGQZ1mVbPManFXAfLoMg/edit)
