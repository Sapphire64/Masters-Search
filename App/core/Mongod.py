# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

import pymongo


class MongoConnection(object):

    def __init__(self):
        try:
            self.connection = pymongo.Connection(auto_start_request=False)
        except pymongo.errors.AutoReconnect:
            self.offline = True
        else:
            self.offline = False
            self.db = self.connection.connections

        # Definitely read the document after the final update completes
        #print str(db.requests.find({'_id': _id}))

    @property
    def requests_limit(self):
        return 25

    def check_user(self, ip, requests_len):
        """
        Function for checking IP.
        Not more than 25 requests per day by each IP.
        """
        if self.offline:
            return (True, '')

        # WRAPPER for MONGODB FUNCTION:
        n_requests = self.check_24h(ip)
        cursor = self.db.banned.find_one({'ip': ip})
        if cursor:
            # If IP in banned list.
            # db.banned.save({'ip': '127.0.0.1'})
            return (False, 'BANNED')

        if n_requests + requests_len <= 25:
            return (True, '')

        return (False, self.requests_limit - n_requests)

    def check_24h(self, ip):
        current_seconds = time()
        cursor = self.db.requests.find({'ip': ip, 'time': {'$gt': current_seconds-84000}}, {'requests': True, 'time': True})
        summary = sum(item['requests'] for item in cursor)
        return summary

    def requests_remaining(self, ip):
        if self.offline:
            return 99
        return self.requests_limit-self.check_24h(ip)

    def add_connection(self, ip, requests_len):
        if self.offline:
            return
        _id = self.db.requests.insert({}, safe=True)
        with self.connection.start_request():
            self.db.requests.update({'_id': _id}, {'$set': {'ip':ip, 'requests': requests_len, 'date': datetime.now().ctime(), 'time' : time()}})
        pass

    def add_history(self, dictionary):
        if self.offline:
            return
        _id = self.db.queries.insert({}, safe=True)
        with self.connection.start_request():
            self.db.queries.update({'_id': _id}, {'$set': dictionary})