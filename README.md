# The Globe  Scraper

The Globe Scraper is a python written news crawler based on the [Scrapy](https://scrapy.org/) framework and is used by the "The Globe" team to get recent news from specific sites.

1. [ Description ](#desc)
2. [ Tech ](#tech)
   1. [ Data Flow ](#dataflow)
3. [Quick Start](#quickstart)
    1. [ Development ](#dev)
    2. [ Deployment ](#deploy)
4. [ License ](#license)


## 1. Description <a name="desc"></a>
This Scraper is built to crawl articles from news organizations such as CNN, BBC, etc. Therefore it requires a list of RSS Feeds which contain news articles. Each article URL will be checked for redundancy and will be further processed under this consideration. As a result, the program outputs a MongoDB-ready dictionary. (For a more detailed procedure see [data flow](#dataflow))

The challenge this product encounters is that every news organization decides on their own how to code their website and it's content. Since the product is still in the development phase this is not done automatically but rather hardcoded in the type of schemas.

## 2. Tech <a name="tech"></a>

The Globe Scraper uses the following open source libraries:

| Library / Language          | Description                                             |
| ----------------------------|---------------------------------------------------------|
| [Scrapy][scrapy]            | Web-crawler engine based on Python                      |
| [PyMongo][pymongo]          | Python-tool to communicate with the MongoDB             |
| [colorlog][colorlog]        | Python-tool makes logs visually understandable          |
| [redis / redisbloom][redis] | check urls for redundancy with a "O(1)" time complexity |

### 2.1. Data Flow <a name="dataflow"></a>
<p align='center'>
<a><img width='50%' src='https://i.ibb.co/tZG2JwZ/theglobe-scaper-data-flow.png'></a>
</p>

[Read more](https://docs.google.com/document/d/1zysHVHg6x2z1DlIxNZfK2KpFGQZ1mVbPManFXAfLoMg/edit?usp=sharing)

## 3. Quick Start <a name="quickstart"></a>

The Globe - Scraper requieres [Python](https://nodejs.org/) >=3.7.4 to run.

```sh
$ git clone https://github.com/Mavial/theglobe-scraper
$ cd theglobe-scraper
```

#### Development <a name="dev"></a>
##### Install all the requiered dependencies
*If you don't have pip installed follow [these instructions](https://www.makeuseof.com/tag/install-pip-for-python/).*

```sh
$ pip install -r requirements.txt
```

##### How to get started

 For a basic start use the following commands.

```sh
# use -s test to disable any interaction with the databases
$ python scrape.py -s test

# use -l debug to enable debug logging
$ python scrape.py -l debug -s test
```

#### Deployment (unstable) <a name="deploy"></a>

##### Install
For a global use on the machine:
*Notice, this approach of installing is unstable and shouldn't be used, yet. Rather use the commands for development.*
```sh
$ pip install .
``` 

##### Run
*The normal script execution should only be used if the script runs correctly and the databases are set up correctly.* 

```sh
$ python scrape.py
```

[scrapy]: <https://scrapy.org/>
[pymongo]: <https://pymongo.readthedocs.io/en/stable/#>
[colorlog]: <https://pypi.org/project/colorlog/>
[redis]: <https://oss.redislabs.com/redisbloom/>


License
----

MIT


