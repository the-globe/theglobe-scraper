import logging
import json
import datetime
import scrapy
import importlib
from urllib.parse import urlparse


class DataHandler():
    """
    Class do handle scraped article Data
    This handler uses two methods to convert the responses.

    1. Schema.org has consistent schemas companies can implement in their webpages.
    2. Through the usual scrapy method -> xpath, this handler tries to acces meta tags.

    For booth methods there are setting files (settings/) that define schemas or selectors (xpath).

    Data Flow (_get_all_data_):
    1. -> __get_schema_ -> __check_schema_

    2. -> __convert_data_   ->  try with schema first
                            ->  then with xpath

    !!!! IMPORTANT !!!!
    The keys in settings/schemas for each schema_type set the fundament of what keys will be in the document.
    Those keys has to be unique and should be a foundation for the 'key <-> function' relation defined in __init__()
    """

    def __init__(self, response, settings, stats):
        self.logger = logging.getLogger(__name__)
        self.settings = settings
        self.stats = stats
        self.response = response
        self.get_func = {}
        self.get_func['name'] = self._get_name_
        self.get_func['title'] = self._get_title_
        self.get_func['title_detail'] = self._get_title_detail_
        self.get_func['author'] = self._get_author_
        self.get_func['summary'] =  self._get_summary_
        self.get_func['content'] = self._get_content_
        self.get_func['tags'] = self._get_tags_
        self.get_func['urlToImg'] = self._get_urlToImg_
        self.get_func['publishedAt'] = self._get_publishedAt_
        self.get_func['modifiedAt'] = self._get_modifiedAt_
        self.get_func['embedUrl'] = self._get_embedUrl_
        self.get_func['type'] = self._get_type_
        self.default_schema_type = self.settings.getdict('DEFAULT')


    def _get_all_data_(self):
        """accesed by spider.articles.py"""
        self.selectors = self.__get_news_settings_()
        if self.selectors == False:
            self.logger.error("__get_news_settings_() returned False")
            return False
        schema = self.__get_schema_()
        if schema == False:
            self.logger.error("__get_schema_() returned False")
            return False
        article = self.__convert_data_(schema)
        if article == False:
            self.logger.error("__convert_data_() returned False")
            return False
        return article

    def __get_schema_(self):
        """
        Private function that tries to get a schema according to schema.org.
        If there is a schema in the given response, it checks it with __check_schema_().
        If there is no schema found the schema_type will be set to DEFAULT (see settings).
        """
        SCHEMA_SELECTORS = self.settings.getlist('SCHEMA_SELECTORS')
        for item in SCHEMA_SELECTORS:
            try:
                schema = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                try:
                    schema = json.loads(schema)
                    if type(schema) == list: # Issue #14
                        raise TypeError
                    if type(schema['@type']) == list: # Issue #14
                        raise AttributeError
                    self.logger.debug(f"Schema {schema['@type']} found in: {self.response.url}")
                except TypeError:
                    self.logger.debug(f"Couldn't find/access schema in. Using default, url: {self.response.url}")
                    self.schema_type = self.default_schema_type
                    return None
                except AttributeError:
                    self.logger.debug(f"@type key of schema is inside a list. Using default, url: {self.response.url}")
                    self.schema_type = self.default_schema_type
                    return None
                else:
                    self.__check_shema_(schema) # Check if schema type exist in settings
                    return schema
        self.logger.critical(f"None of the SCHEMA_SELECTORS worked for: {self.response.url} ")
        return False


    def __check_shema_(self, schema):
        """
        This private function checks the given schema on existence in the settings.
        If this schema doesn't exist it will through a warning and set the schema_type to DEFAULT.
        """
        schema_type = self.settings.getdict(schema['@type'].upper())
        if not schema_type:
            self.logger.warning(f"There is no existing Schema sample for the {schema['@type']} type. Using default, url: {self.response.url}")
            self.schema_type = self.default_schema_type
            return False
        else:
            type = self.default_schema_type
            type.update(schema_type)
            self.schema_type = type
            self.logger.debug(f"Schema {schema['@type']} does exist. Default got updated for {self.response.url}")
            return schema


    def __get_news_settings_(self):
        try:
            parsed_uri = urlparse(self.response.url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            settings_import = '.settings.site_selectors.' + self.settings.getdict('NEWS_ORGANISATIONS')[domain]
            selectors = importlib.import_module(settings_import, package='theglobe')
        except Exception:
            self.logger.error(f"Error while setting specified settings for 'domain'", exc_info=True)
            return False
        else:
            return selectors


    def __convert_data_(self, schema=None):
        """
        This private function converts the given response to a defined document/dict according the schemas in settings/schemas.
        For more information on the schemas take a look at the settings file.

        First this function gets all keys from the schema_type and loops through them.
            If the value of the key is an empty list ([]) the function will instantly call the xpath converter.
            Else it tries to acces the schema.org tag of the response with the given values inside the list.
                if that fails the xpath converter is called again. (This should not happen, because the local and response schema_type should be the same)

        Important is to understand that this function first tries to get the data for a key from the schema tag from a response.
        When the schema_type is set to DEFAULT every value of a looped key is an empty list -> Hence xpath is called instantly.
        """
        keys = self.schema_type.keys()
        data = {}
        for key in keys:
            if self.schema_type[key]['list'] == []:
                value = self.__convert_response_xpath_(key)
            else:
                value = schema
                for x in self.schema_type[key]['list']:
                    try:
                        value = value[x]
                    except KeyError:
                        try:
                            self.logger.warning(f"{schema['@type']} acces problem [key: {key} -> {x}] Trying if there is a '@list' key.")
                            new_value = []
                            for item in value['@list']:
                                new_value.extend(item[x])
                            value = new_value
                        except KeyError:
                            self.logger.warning(f"{schema['@type']} acces problem [key: {key} -> {x}] No '@list' key found. Using xpath. [ {self.response.url} ]", exc_info=False)
                            value = self.__convert_response_xpath_(key)
                            break
                        else:
                            self.logger.info(f"{schema['@type']} acces granted through '@list' key.")

            """TODO If this function gets it's date values from the schema.org tag it's not formatted -> Idially this should be done better than here."""
            if key == "publishedAt" or key == "modifiedAt":
                if value != "N/A":
                    value = self._date_formatter_(value, key)
            data[key] = value

        """TODO put a schema check here (pip install schema / pip install jsonschema)"""
        return data


    def __convert_response_xpath_(self, key):
        """
        This function calls according to the given key a function saved in the get_func dict.
            !!! Example:
                key 'name' gets passed:
                    get_func has to have same key -> 'name' with value -> _get_name_
        The dict is defined in the __init__ function of this class.
        """
        try:
            value = self.get_func[key]()
        except KeyError:
            self.logger.error(f"get_func acces Error. No value for {key}", exc_info=True)
            self.stats.inc_value(f'function_not_found/{key}')
            return "N/A"
        else:
            if value == "N/A":
                self.logger.info(f"None of the Selectors worked [{key}] [ {self.response.url} ]")
                self.stats.inc_value(f'no_data_found/{key}')
            return value


    def _get_name_(self):
        """Get the name of the Newspaper."""
        NAME_SELECTORS = self.selectors.get('NAME_SELECTORS')
        for item in NAME_SELECTORS:
            try:
                name = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return name
        return("N/A")


    def _get_title_(self):
        """Get the title of the article."""
        TITLE_SELECTORS = self.selectors.get('TITLE_SELECTORS')
        for item in TITLE_SELECTORS:
            try:
                title = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return title
        return("N/A")


    def _get_title_detail_(self):
        """
        Get a detailed title of the article.
        Mostly called "description".
        """
        TITLE_DETAIL_SELECTORS = self.selectors.get('TITLE_DETAIL_SELECTORS')
        for item in TITLE_DETAIL_SELECTORS:
            try:
                title_detail = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return title_detail
        return("N/A")

    def _get_author_(self):
        """
        Get the author of the article.
        This can sometimes be a bit tricky:
        BBC only has itself as author of the article.
        """
        AUTHOR_SELECTORS = self.selectors.get('AUTHOR_SELECTORS')
        for item in AUTHOR_SELECTORS:
            try:
                author = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return author
        return("N/A")

    def _get_summary_(self):
        """
        Get a summary of the article.
        Sometimes the articles only have a title and description, but no summary.
        """
        SUMMARY_SELECTORS = self.selectors.get('SUMMARY_SELECTORS')
        for item in SUMMARY_SELECTORS:
            try:
                summary = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return summary
        return("N/A")


    def _get_content_(self):
        """
        Get the whole content of the article.
        TODO This is still pretty hard to do
        regarding to the fact that there are many different article types.
        """
        return("N/A")
        CONTENT_SELECTORS = self.selectors.get('CONTENT_SELECTORS')
        for item in CONTENT_SELECTORS:
            try:
                content = self.response.xpath(item).getall()
                content = ''.join(map(str, content))
                if content == '':
                    raise Exception
            except Exception:
                continue
            else:
                return content
        return("N/A")


    def _get_tags_(self):
        """
        Get the keywords/tags.
        Some websites have keyword/tags regardning to the articles topic.
        """
        TAG_SELECTORS = self.selectors.get('TAG_SELECTORS')
        for item in TAG_SELECTORS:
            try:
                tags = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return tags
        return("N/A")


    def _get_urlToImg_(self):
        """
        Get the main Image of the article.
        Articles can have more than one picture,
        but this method only wants to get the main picture.
        """
        IMAGE_SELECTORS = self.selectors.get('IMAGE_SELECTORS')
        for item in IMAGE_SELECTORS:
            try:
                url_to_img = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return url_to_img
        return("N/A")


    def _get_publishedAt_(self):
        """
        Get the published date of the article.
        Articles can have many different date data.
        Most important, though, is when the article got published.
        """
        PUB_DATE_SELECTORS = self.selectors.get('PUB_DATE_SELECTORS')

        for item in PUB_DATE_SELECTORS:
            try:
                response_date = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                # form_date = self._date_formatter_(response_date)
                # if form_date:
                    # return form_date
                if response_date:
                    return response_date
        return("N/A")


    def _get_modifiedAt_(self):
        """
        Get the modified date of the article.
        Articles can have many different date data.
        """
        MOD_DATE_SELECTORS = self.selectors.get('MOD_DATE_SELECTORS')

        for item in MOD_DATE_SELECTORS:
            try:
                response_date = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                # form_date = self._date_formatter_(response_date)
                # if form_date:
                    # return form_date
                if response_date:
                    return response_date
        return("N/A")


    def _date_formatter_(self, date, key):
        DATE_FORMATS = self.settings.getlist('DATE_FORMATS')
        if date == None:
            return False
        for format in DATE_FORMATS:
            try:
                form_date = datetime.datetime.strptime(date, format)
            except Exception:
                continue
            else:
                return form_date
        self.logger.error(f"Format error [{key}] ('{date}') [ {self.response.url} ]")
        return date

    def _get_embedUrl_(self):
        return 'N/A'

    def _get_type_(self):
        """
        Get the type of the article.
        Video. Article. etc.
        """
        TYPE_SELECTORS = self.settings.getlist('TYPE_SELECTORS')
        for item in TYPE_SELECTORS:
            try:
                type = self.response.xpath(item).get()
            except Exception:
                continue
            else:
                return type
        return("N/A")