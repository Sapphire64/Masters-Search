# -*- coding: utf-8 -*-
from App.Settings import YANDEX_PATH

import re

class SiteQueryProcessor(object):
    """Module for processing queries and search results.

    Functions with arguments 'match' are POST processing functions.
    Functions with arguments 'query' are PRE processing functions.
    """

    def only_digits(self, match):
        """
        Get only digits from the whole match, i.e.
            '32 300,00' will be returned as '3230000'
        """
        match = match.replace('&#160;', '')
        return str(''.join(letter for letter in match if letter.isdigit()))

    def safety_check(self, query):
        """
        Simple test to block bad behaviour in search queries.

        Like: http://example.com/q?=(query?blah=some_bad_param_etc)
        """
        if not any(item in query for item in ['?', '!', '=', '&']):
            return True
        return False

    def spaces_to_pluses(self, query):
        """
        Simply: ' te st ' >>>> '+te+st+'
        """
        return '+'.join(query.split())

    def spaces_to_sign(self, query):
        """
        Simply: ' te st ' >>>> '%20te%20st%20'
        """
        return '%20'.join(query.split())

    def determine_page_charset(self, pagedata):
        template = re.compile(r'charset=(.+?)">')
        return template.search(pagedata).group(1)

    def yandex_query(self, downloader, xml):
        page = downloader.get_web_page(YANDEX_PATH, xml)
        print page
        return page.encode('UTF-8')

    def yandex_xml(self, query):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
                <request>
                	<query>%s</query>
                </request>""" % query
        return xml
