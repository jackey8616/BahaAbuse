import re

from .summary import Summary
from .main import Main
from .count import Count
from .time import Time
from .content import Content

class Article(object):

    def __init__(self, html, serial=None):
        self.summary = Summary(self, html) if html else serial['summary']
        self.main = Main(self, html) if html else serial['main']
        self.count = Count(self, html) if html else serial['count']
        self.time = Time(self, html) if html else serial['time']
        self.content = Content(self) if html else serial['content']
        self.detail = self.articleDetail()

    def isSticky(self):
        return self.summary.rowSticky

    def timeOffset(self, article):
        return self.time.replyTime - article.time.replyTime

    def articleDetail(self):
        url = self.main.url
        if url:
            php = url.split('?')[0]
            bsn = int(re.search('bsn=[0-9]+&', url).group()[4:-1])
            sna = int(re.search('snA=[0-9]+&', url).group()[4:-1])
            tnum = int(re.search('tnum=[0-9]+', url).group()[5:])
            return { 'php': php, 'bsn': bsn, 'snA': sna, 'tnum': tnum }
        else:
            return { 'php': None, 'bsn': -1, 'snA': -1, 'tnum': -1 }

    def crawlContent(self):
        self.content.crawlContent(self.detail)

    def __str__(self):
        return str(self.summary) + ' / ' + str(self.main) + ' / ' + str(self.count) + ' / ' + str(self.time)

    def toJson(self):
        return {
            'detail': self.detail,
            'summary': self.summary.toJson(),
            'main': self.main.toJson(),
            'count': self.count.toJson(),
            'time': self.time.toJson(),
            'content': self.content.toJson()
        }

    @staticmethod
    def fromJson(doc):
        article = Article(html=None, serial={
            'summary': Summary.fromJson(doc['summary']),
            'main': Main.fromJson(doc['main']),
            'count': Count.fromJson(doc['count']),
            'time': Time.fromJson(doc['time']),
            'content': Content.fromJson(doc['content'])
        })
        article.summary.article = article
        article.main.article = article
        article.count.article = article
        article.time.article = article
        article.content.article = article
        article.detail = article.articleDetail()
        return article

    def keyJson(self):
        keyJson = {}
        for key, val in self.detail.items():
            keyJson['detail.' + key] = val
        for key, val in self.summary.toJson().items():
            keyJson['summary.' + key] = val
        for key, val in self.main.toJson().items():
            keyJson['main.' + key] = val
        for key, val in self.count.keyJson().items():
            keyJson['count.' + key] = val
        return keyJson

