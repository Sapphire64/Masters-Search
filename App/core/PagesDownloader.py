# -*- coding: utf-8 -*-
from core.SiteQueryProcessors import SiteQueryProcessor
from core.Downloader import BasicDownloader
from random import  randint
from datetime import date
from time import sleep

import traceback
import logging
import time
import sys
import re


class PagesDownloader(object):

    def __init__(self, mongo_connection):

        self.mongod = mongo_connection
        self.processors = SiteQueryProcessor()
        self.downloader = BasicDownloader()

        logging.basicConfig(filename='logs/access.log', level=logging.INFO, format='%(asctime)s  %(message)s')

        self.search_systems = [
                {'name': 'Yandex', 'query': self.processors.yandex_query, 'face_query': 'http://yandex.ua/yandsearch?text=',
                 'search_pattern': re.compile(r'<found priority="phrase">(\d+)</found>'),
                 'processor': None, 'preprocessor': self.processors.yandex_xml},
                {'name': 'Meta.ua', 'query': 'http://meta.ua/ex/search.asp?q=', 'search_pattern': re.compile(r"<div class='found_info' >.*?<span>(.+?)</span>"),
                 'processor': self.processors.only_digits, 'preprocessor': None},
            # You can add here another one
        ]

    def get_results(self, search_queries):
        """ One function to ask search systems, generate HTML output.

            Give it your queries as a list and you will recieve complete HTML
            with table of results. Easy and useful.
        """
        search_systems = self.search_systems
        # HTML results file
        results_list = []
        # Short alias for actively used function.
        append = results_list.append

        # Adding current date.
        current_date = date.today()
        append(current_date.strftime('<div align="center"><h3>Результаты поиска на %d.%m.%Y</h3></div><br>'))
        # Generating headers for table.
        append('<table class="table table-bordered">\n<thead>\n<tr>\n<th>Запрос</th>')
        for system in search_systems:
            append("<th>%s</th>" % system['name'])
        append('</tr>\n</thead>')

        # Generating data output body table.
        append('<tbody>')
        for query in search_queries:
            # Is query safe for making requests
            if not self.processors.safety_check(query):
                # If not - skip this word.
                continue
            # Initializing dict to store data in mongo db.
            historical_data = {}
            # New row with query text
            append('<tr>\n<td>%s</td>' % query)
            # Looping through search systems
            for system in search_systems:
                # Applying preprocessor functions
                if system['preprocessor']:
                    query_text = system['preprocessor'](query)
                else:
                    # If no function specified - use default one.
                    query_text = self.processors.spaces_to_sign(query)
                append('<td>')
                try:
                    if type(system['query']) is str:
                        # Default queries are 'str' type.
                        pageData = self.downloader.get_web_page(system['query']+query_text)
                    else:
                        # Non-default are functions.
                        pageData = system['query'](self.downloader, query_text)
                    # REGEXP check of output data.
                    a = system['search_pattern'].search(pageData)
                    # if no match - we've got exception.
                    if a:
                        a = a.groups()[0]
                        try:
                            a.encode('UTF-8')
                        except:
                            pass
                        # Applying post-processing if required.
                        if system['processor']:
                            result = system['processor'](a)
                        else:
                            result = a
                    else:
                         raise Exception('Pattern error.')
                except Exception as e:
                    # Log our error.
                    logging.info(" 'ERROR' => %s ~ %s ~ %s" % (system['name'], e,query))

                    # Result will give user message to try his request manually.
                    result = 'Ошибка, попробуйте вручную'
                    if __debug__:
                        # generating error's traceback (because errors are really silent here).
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print "*** print_tb:"
                        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                        print "*** print_exception:"
                        traceback.print_exception(exc_type, exc_value, exc_traceback,
                            limit=2, file=sys.stdout)
                        print "*** print_exc:"
                        traceback.print_exc()
                        print "*** format_exc, first and last line:"
                        formatted_lines = traceback.format_exc().splitlines()
                        print formatted_lines[0]
                        print formatted_lines[-1]
                        print "*** format_exception:"
                        print repr(traceback.format_exception(exc_type, exc_value,
                            exc_traceback))
                        print "*** extract_tb:"
                        print repr(traceback.extract_tb(exc_traceback))
                        print "*** format_tb:"
                        print repr(traceback.format_tb(exc_traceback))
                        print "*** tb_lineno:", exc_traceback.tb_lineno
                else:
                    pass
                    #historical_data[system] = result
                finally:
                    result = '<a href="%s%s">%s</a>' % (system['query'] if type(system['query']) is str else system['face_query'],
                                                      query, result)
                    append(result)
                append('</td>')
            append('</tr>')
            # If requests (any) were successful -> log it in DB for future generations ^_^
            if historical_data:
                # Optimization - we store query text only if queries were successful.
                historical_data['query'] = query
                historical_data['time'] =time.time()
                self.mongod.add_history(historical_data)
            # Weird sleep function to look less like bot.
            sleep(randint(11000,28000)/10000)

        append('</table>')
        # Join all our outputs as almost good formatted html :)
        output_text = '\n'.join(results_list)
        # Add to our html section with source code for user to add to it's own page.
        output_text = output_text + '\n<br><br>\n' + self.generate_code_tag(output_text)
        return output_text

    def generate_code_tag(self, html):
        " Serving <pre> tag. Tag <pre> needs '<' and '>' to be escaped."
        html =  html.replace('<', '&lt;').replace('>', '&gt;')
        html = '<div align="center"><h3>Код для вставки на свою страницу</h3></div><br>' \
                '<pre class="prettyprint lang-html">' + html + '</pre>'
        return html