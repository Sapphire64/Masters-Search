#/usr/bin/env python -OO
# -*- coding: UTF-8 -*-

# Twisted functions import
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
from twisted.web import  resource, http
# Internal functions import
from core.PagesDownloader import PagesDownloader
from core.Mongod import MongoConnection
from core.PagesRenderer import Renderer
# Standard functions import
import logging
import sys
import cgi

port = 8080

class ListenResource(resource.Resource):
    """
    Web server basic class for handling POST and GET requests from the users.
    """
    isLeaf = True


    def render_GET(self, request, thanks=False):
        """
        Main GET requests handler. We have only one page for GET request w/o
        data, so we care only about '/' query with only option - different
        upper banner. After user enters new search system he will see
        a 'THANK YOU' banner at the place of current EULA banner.

        This behaviour is handle by 'thanks' flag.

        """
        ip = request.getClientIP()
        if not thanks:
            logging.info(" 'GET %s' => %s <=" % (request.path, ip))
        return self.renderer.render_index(self.mongod.requests_limit, self.mongod.requests_remaining(ip),
                                          thanks)
        #return '<html><body><form method="POST"><input name="the-field"
        # type="text" /></form></body></html>'

    def render_POST(self, request):
        """
        POST requests handler. Hardly used to get data from the index page
        and then process it.

        As an output user will see special page with table of values.
        """
        # Block 1: if user adds new search system
        try:
            s_name, s_addr, s_regexp = (cgi.escape(request.args["s_name"][0]),
                                        cgi.escape(request.args["s_addr"][0]),
                                       cgi.escape(request.args["s_regexp"][0]))
        except Exception as e:
            pass
        else:
            logging.info((" 'APPEND' => " ' ~ '.join([s_name, s_addr, s_regexp])))
            thanks = True if s_addr else False
            return self.render_GET(request, thanks)

        # Block 2: if user clicked other submit button - for the main form.
        try:
            requests = set(cgi.escape(request.args["queries"][0]).split('\r\n'))
        except Exception as e:
            logging.info(" 'ERROR' => %s" % e)
            return 'Error'
        if not all(requests):
            return self.render_GET(request)
        ip = request.getClientIP()
        requests_len = len(requests)
        allowed_to_connect = self.mongod.check_user(ip, requests_len)
        text = 'Error' # If user will see this text - something ugly happened.

        if allowed_to_connect[0]:
            self.mongod.add_connection(ip, requests_len)
            counters = self.downloader.get_results(requests)
            logging.info(" 'POST' => %s <=" % ip)
            text = '%s \n %s' % (self.renderer.render_return_hyperlink(),
                                 counters)
        else:
            if allowed_to_connect[1] == 'BANNED':
                text = '<div align="center"><h3>Вам запрещено делать запросы.</h3></div><br>'
            elif allowed_to_connect[1] > 0:
                text = '<div align="center"><h3>Ваши %s запроса не могут быть выполнены,'\
                       ' т.к. у вас осталось лишь %s запросов.</h3></div><br>' % (requests_len, allowed_to_connect[1])
            else:
                text = '<div align="center"><h3>Вы превысили количество' \
                       ' доступных запросов за последние 24 часа. Попробуйте на следующий день.</h3></div><br>'

        return "\n".join([self.renderer.render_results_header(), text, self.renderer.render_results_footer()])
        #return '<html><body>You submitted: %s</body></html>' % (cgi.escape(request.args["the-field"][0]),)

    def __init__(self):
        """
        Init.
        """
        self.renderer = Renderer()
        self.mongod = MongoConnection()
        self.downloader = PagesDownloader(self.mongod)

        print ('Server started at http://0.0.0.0:%s' % port)

class File(File):
    " Rewriting standard class to disable directory listing"
    def directoryListing(self):
        raise http.HTTPError(responsecodes.FORBIDDEN)



logging.basicConfig(filename='App/logs/access.log', level=logging.INFO, format='%(asctime)s  %(message)s')

root = Resource()
root.putChild('bootstrap', File('./App/bootstrap'))
root.putChild('images', File('./App/images'))
root.putChild('', ListenResource())

factory = Site(root)
#f = protocol.ServerFactory()
try:
    reactor.listenTCP(port, factory)
    reactor.run()
except Exception as e:
    sys.exit('Error: %s' % e)