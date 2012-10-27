# -*- coding: utf-8 -*-

class Renderer(object):
    """
    Simple html pages rendered for DonNTU masters' site project.
    """
    LICENSE = ''
    '''<div class="alert">
            <strong>Условия использования:</strong> Пользоваться приложением разрешено только студентам, обучающимся в магистратуре ДонНТУ и изучающим курс "Интернет-технологии".
        </div>'''
    THANKS = '''<div class="alert alert-success"><strong>Спасибо!</strong> Запрос на добавление поисковой системы будет обработан администратором.</div>'''

    def render_index(self, max_requests, requests_remaining, thanks=False):
        header = self.LICENSE if not thanks else self.THANKS
        self.page = self.index_page % {'header': header, 'number': requests_remaining, 'max_requests': max_requests}
        return self.page

    def render_results_header(self):
        return self.results_page_header

    def render_results_footer(self):
        return self.results_page_footer

    def render_return_hyperlink(self):
        return self.return_hyperlink

    def load_pages(self):
        self.results_page_header = open('App/templates/answer_header.html', 'r').read()
        self.results_page_footer = open('App/templates/answer_footer.html', 'r').read()
        self.return_hyperlink = '<div align="center"><p><a href="/">Вернуться на главную страницу</a></p></div>\n<br>'
        self.index_page = open('App/templates/index_page.html', 'r').read()

    def __init__(self):
        self.load_pages()
