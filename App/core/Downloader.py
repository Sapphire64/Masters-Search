from random import choice

import urllib2

class BasicDownloader(object):

    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (X11; Linux i686) AppleWebKit/534.34 (KHTML, like Gecko) rekonq Safari/534.342011-10-16 20:21:01',
            ]

    def get_user_agent(self):
        return choice(self.user_agents)

    def get_web_page(self, address, data=None, proxy=None):

        user_agent = self.get_user_agent()
        page_address = address

        pageHandler  = urllib2.build_opener(urllib2.HTTPHandler)

        requestData = urllib2.Request(page_address, data,  {'Accept-Language':'ru-ru,ru;q=0.5','User-Agent': user_agent})
        requestHandler = pageHandler.open(requestData)

        pageData = requestHandler.read()

        try:
            pageData = pageData.decode('utf-8')
        except Exception as e:
            #print self.processors.determine_page_charset(pageData)
            #pageData = pageData.decode()
            print '%s' % e

        requestHandler.close()

        return pageData
