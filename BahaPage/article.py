import re

from .summary import Summary
from .main import Main
from .count import Count
from .time import Time
from .content import Content

class Article(object):

    def __init__(self, html):
        self.summary = Summary(self, html)
        self.main = Main(self, html)
        self.count = Count(self, html)
        self.time = Time(self, html)
        self.content = Content(self)

    def isSticky(self):
        return self.summary.rowSticky

    def timeOffset(self, article):
        return self.time.replyTime - article.time.replyTime

    def __str__(self):
        return str(self.summary) + ' / ' + str(self.main) + ' / ' + str(self.count) + ' / ' + str(self.time)

    def toJson(self):
        return {'summary': self.summary.toJson(), 'main': self.main.toJson(), 'count': self.count.toJson(), 'time': self.time.toJson(), 'content': self.content.toJson()}

    def keyJson(self):
        keyJson = {}
        for key, val in self.summary.toJson().items():
            keyJson['summary.' + key] = val
        for key, val in self.main.toJson().items():
            keyJson['main.' + key] = val
        for key, val in self.count.keyJson().items():
            keyJson['count.' + key] = val
        return keyJson

