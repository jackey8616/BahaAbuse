from threading import Thread, Event
from datetime import datetime
import requests

from BahaPage.bPage import BPage

class Crawler(Thread):

    def __init__(self, col, name, url):
        Thread.__init__(self)
        self.col = col[name]
        self.url = url
        self.sleep = 0
        self.stopped = Event()

    def start(self):
        print('[{}] {} seconds will start crawl'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'), self.sleep))
        super(Crawler, self).start()

    def run(self):
        while not self.stopped.wait(self.sleep):
            print('[{}] Looping crawl'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
            updateOffset = self.crawl()
            self.sleep = updateOffset if updateOffset and self.sleep != updateOffset else self.sleep + 60
            print('  => Sleep: {}'.format(self.sleep))

    def crawl(self):
        response = requests.get(self.url)
        bPage = BPage(self.col, response.text)
        return bPage.lastUpdateOffset()

