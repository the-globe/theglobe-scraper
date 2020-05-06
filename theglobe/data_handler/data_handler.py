import logging
import json
import datetime
import scrapy
import importlib
from urllib.parse import urlparse
import ast
import copy


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
        self.selectors = copy.deepcopy(self.settings.getdict('DEFAULT_SELECTORS')) # empty lists for xpath and schema_org
        self.selectors_xpath_key = self.settings.get("XPATH_KEY")
        self.selectors_schema_org_key = self.settings.get("SCHEMA_ORG_KEY")
        self.keys = self.selectors.keys()


    def _get_all_data_(self):
        """accesed by spider.articles.py"""
        if self.__get_site_settings_() == False:
            self.logger.warning("__get_site_settings_() returned False")
            return False
        schema_org = self.__get_schema_org_()
        if schema_org == False:
            self.logger.warning("__get_schema_org_() returned False")
            return False
        article = self.__convert_data_(schema_org)
        if article == False:
            self.logger.warning("__convert_data_() returned False")
            return False
        return article


    def __get_schema_org_(self):
        """
        Private function that tries to get a schema according to schema.org.
        If there is a schema in the given response, it checks it with __check_schema_().
        If there is no schema found the schema_type will be set to DEFAULT (see settings).
        """
        SCHEMA_ORG_SELECTOR = self.settings.get('SCHEMA_ORG_SELECTOR')
        try:
            index = int(self.schema_handling['index'])
            list_check = self.schema_handling['list_check']

            schema = self.response.xpath(SCHEMA_ORG_SELECTOR).getall()
            if schema == None or schema == []:
                self.logger.info(f'No schema found on [ {self.response.url} ] Using default')
                return None

            schema = schema[index]
            try:
                schema = json.loads(schema)
            except Exception:
                self.logger.warning(f"Couldn't load schema with json. url: [ {self.response.url} ]", exc_info=False)
                raise Exception
            if list_check == True:
                try:
                    if type(schema) != list:
                        raise TypeError
                except Exception:
                    self.logger.warning("list_check = True, but it's not a list")
                else:
                    list_index = self.schema_handling['list_index']
                    if list_index != None:
                        schema = schema[list_index]
                    # else:
                    #     self.logger.info(schema)
                    #     for item in schema:
                    #         try:
                    #             item = dict(item)
                    #         except Exception:
                    #             self.logger.warning(f"Couldn't load schema with dict [ {self.response.url} ]\nItem: {item}", exc_info=False)
                    #             raise Exception
                    #         else:
                    #             schema = item
            if type(schema['@type']) == list:
                type_is_list = True
            else:
                type_is_list = False
        except Exception:
            self.logger.error(f"schema handling went wrong. url: [ {self.response.url} ]", exc_info=True)
            return False
        else:
            if type_is_list == True:
                self.schema_at_type = schema['@type'][0]
            else:
                self.schema_at_type = schema['@type']
            self.logger.debug(f"Schema {self.schema_at_type} found in: {self.response.url}")
            if self.__check_shema_org_type_(schema): # Check if schema type exist in settings
                return schema
            else:
                return None
        self.logger.error(f"None of the SCHEMA_SELECTORS worked for: {self.response.url} ")
        return None


    def __check_shema_org_type_(self, schema):
        """
        This private function checks the given schema on existence in the settings.
        If this schema doesn't exist it will throw a warning -> return False.
        If the type does exist it will add the selectors to self.selectors with add_to_selectors function -> True
        """
        schema_type_selectors = self.settings.getdict(self.schema_at_type.upper())
        if not schema_type_selectors:
            self.logger.warning(f"There is no existing Schema sample for the {self.schema_at_type} type. Using default, url: {self.response.url}")
            return False
        else:
            self.__add_to_selectors_(self.selectors_schema_org_key, schema_type_selectors)
            self.logger.debug(f"Schema {self.schema_at_type} does exist. Default got updated for {self.response.url}")
            return True


    def __get_site_settings_(self):
        """
            get site specific settings when applicable.
            adds xpath_selectors to self.selectors with add_to_selectors function
            creates self.schema_handling
        """
        try:
            parsed_uri = urlparse(self.response.url)
            domain = '{uri.netloc}'.format(uri=parsed_uri)
            settings_import = '.settings.site_settings.' + self.settings.getdict('NEWS_ORGANISATIONS')[domain]
            site_settings = importlib.import_module(settings_import, package='theglobe')
            xpath_selectors = site_settings.xpath_selectors
            self.__add_to_selectors_(self.selectors_xpath_key, xpath_selectors)
            self.schema_handling = site_settings.schema_handling
        except Exception:
            self.logger.error(f"Loading domain specific settings failed [ {domain} ] [ {self.response.url} ]", exc_info=True)
            return False
        else:
            return True


    def __add_to_selectors_(self, selector_type, selectors):
        keys = selectors.keys()
        try:
            for key in keys:
                self.selectors[key].update({selector_type : selectors[key]})
        except Exception:
            self.logger.error(f"Couldn't add '{selector_type}' selectors to self.selectors [ {self.response.url} ]", exc_info=True)
            return False
        else:
            return True




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
        data = {}
        for key in self.keys:
            if self.selectors[key][self.selectors_schema_org_key] == []:
                value = self.__get_xpath_value_(key)
            else:
                value = self.__get_schema_org_value_(key, schema)
                if value == False:
                    value = self.__get_xpath_value_(key)

            """TODO If this function gets it's date values from the schema.org tag it's not formatted -> Idially this should be done better than here."""
            if key == "publishedAt" or key == "modifiedAt":
                if value != "N/A":
                    value = self._date_formatter_(value, key)
            data[key] = value
            if key == "url" and value == "N/A":
                value = self.response.url

        """TODO put a schema check here (pip install schema / pip install jsonschema)""" # can also be done with mongodb
        return data


    def __get_schema_org_value_(self, key, schema):
        indices_length = len(self.selectors[key][self.selectors_schema_org_key])
        key_list = self.selectors[key][self.selectors_schema_org_key]
        try:
            value = schema[key_list[0]]
        except TypeError:
            self.logger.error(f"{self.schema_at_type} Problem with [main key: {key} -> key_list: {key_list}] Using xpath. [ {self.response.url} ]")
        except KeyError:
            self.logger.warning(f"{self.schema_at_type} acces problem [main key: {key} -> {key_list[0]}] Key doesn't exist. Using xpath. [ {self.response.url} ]", exc_info=False)
            return False
        else:
            try:
                for x in range(1, indices_length + 1):
                    value_type = type(value)
                    if indices_length > x:
                        if value_type == dict:
                            try:
                                value = value[key_list[x]]
                            except KeyError:
                                try:
                                    value = value['@list']
                                except Exception:
                                    ''' TODO better error handling here! '''
                                    self.logger.warning(f"{self.schema_at_type} access problem [main key: {key} -> {key_list[0:]}] [value: {value}] Using xpath. [ {self.response.url} ]")
                                    return False
                                else:
                                    new_value = []
                                    for item in value:
                                        new_value.extend([item[key_list[x]]])
                                    value = new_value
                            continue
                        elif value_type == list:
                            if type(value[0]) == dict:
                                new_value = []
                                for item in value:
                                    new_value.extend([item[key_list[x]]])
                                value = new_value
                                continue
                            if type(value[0]) == str:
                                continue
                            if type(value[0]) == list:
                                self.logger.warning(f"{self.schema_at_type} access problem [main key: {key} -> {key_list[0:]}] list in list. [value: {value}] Using xpath. [ {self.response.url} ]")
                                return False
                        elif value_type == str:
                            continue
                    elif indices_length == x:
                        if value_type == str:
                            return value
                        elif value_type == dict:
                            self.logger.warning(f"{self.schema_at_type} access problem [main key: {key} -> {key_list[0:]}] There is a dict but no keys left in schema type. [dict: {value}] Using xpath. [ {self.response.url} ]")
                            return False
                        elif value_type == list:
                            seperator = ", "
                            new_value = seperator.join(value)
                            return new_value
            except Exception:
                self.logger.error(f"{self.schema_at_type} Something unexpected went wrong. Using xpath. [main key: {key}] [ {self.response.url} ]", exc_info=True)
                return False


    def __get_xpath_value_(self, key):
        try:
            SELECTORS = self.selectors[key][self.selectors_xpath_key]
        except KeyError:
            self.logger.warning(f"Failure when trying to get selectors [{key}]", exc_info=True)
            self.stats.inc_value(f'selectors_not_found/{key}')
        else:
            for item in SELECTORS:
                try:
                    value = self.response.xpath(item).get()
                except Exception:
                    self.logger.error('Error', exc_info=True)
                else:
                    if value == None:
                        continue
                    else:
                        return value
            self.logger.debug(f"None of the Selectors worked [{key}] [ {self.response.url} ]")
        self.stats.inc_value(f'no_data_found/{key}')
        return('N/A')


    # def _get_content_(self): # not deleted yet, because to get and format the content is a different proccess
    #     """
    #     Get the whole content of the article.
    #     TODO This is still pretty hard to do
    #     regarding to the fact that there are many different article types.
    #     """
    #     return("N/A")
    #     CONTENT_SELECTORS = self.selectors.get('CONTENT_SELECTORS')
    #     for item in CONTENT_SELECTORS:
    #         try:
    #             content = self.response.xpath(item).getall()
    #             content = ''.join(map(str, content))
    #             if content == '':
    #                 raise Exception
    #         except Exception:
    #             continue
    #         else:
    #             if content == None:
    #                 continue
    #             else:
    #                 return content
    #     return("N/A")

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