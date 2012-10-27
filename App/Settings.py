

YANDEX_PATH = 'http://xmlsearch.yandex.ru/xmlsearch?user=YOUR_NAME&key=YOUR_KEY'

SEARCH_SYSTEMS = [
        {'name': 'Yandex', 'query': self.processors.yandex_query, 'face_query': 'http://yandex.ua/yandsearch?text=',
         'search_pattern': re.compile(r'<found priority="phrase">(\d+)</found>'),
         'processor': None, 'preprocessor': self.processors.yandex_xml},
        {'name': 'Meta.ua', 'query': 'http://meta.ua/ex/search.asp?q=', 'search_pattern': re.compile(r"<div class='found_info' >.*?<span>(.+?)</span>"),
         'processor': self.processors.only_digits, 'preprocessor': None},
]