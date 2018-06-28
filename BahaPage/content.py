import re, requests

class Content(object):

    def __init__(self, article):
        self.article = article
        self.html = None

    def crawl(self):
        response = requests.get(self.article.main.url)
        print(response.text)

    def __str__(self):
        return 'Html: ' + str(self.html)

    def toJson(self):
        return {'html': str(self.html)}

