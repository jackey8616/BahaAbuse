from threading import Thread
import requests

from BahaPage.bPage import BPage

class Crawler(Thread):

    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        pass

    def crawl(self):
        response = requests.get(self.url)
        bPage = BPage(response.text)

