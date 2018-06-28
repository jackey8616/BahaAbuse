from threading import Thread, Event
from datetime import datetime
import requests

from BahaPage.bPage import BPage

class Crawler(Thread):

    def __init__(self, col, name, url, bsn):
        Thread.__init__(self)
        self.col = col[name]
        self.url = url
        self.bsn = bsn

        self.sleep = 0
        self.stopped = Event()

    def run(self):
        while not self.stopped.wait(self.sleep):
            print('[{}] Looped crawl'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
            articleCount, updateOffset = self.crawl()
            self.sleep = updateOffset if updateOffset and self.sleep != updateOffset else self.sleep + 60
            print('  => Crawler Sleep: {}'.format(self.sleep))

    def crawl(self):
        response = requests.get(self.url)
        self.bPage = BPage(self.col, response.text, self.bsn)
        self.bPage.script()
        self.bPage.subboard()
        articleCount = self.bPage.articleList()
        return articleCount, self.bPage.lastUpdateOffset()

