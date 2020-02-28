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

            selectors       # settings file for all the selectors (article)

        spiders/          # a directory with all the spiders
            __init__.py

            articles.py   # This spider Scrapes through news websites to get articles.
```

# Project Architecture (Data Flow)
[Google Docs](https://docs.google.com/document/d/1zysHVHg6x2z1DlIxNZfK2KpFGQZ1mVbPManFXAfLoMg/edit)