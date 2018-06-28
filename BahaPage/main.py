import re

class Main(object):

    def __init__(self, article, html):
        self.article = article
        mainHtml = re.search('<td class=\"b-list__main\">.*?</td>', html, flags=re.DOTALL).group(0)
        if 'href' in mainHtml:
            self.title = re.search('>.*?</a>', mainHtml).group(0)[1:-4]
            self.url = re.search('href=\".*?\"', mainHtml).group(0)[6:-1]
        else:
            self.title = re.search('>.*?</span>', mainHtml).group(0)[1:-7]
            self.url = None

    def __str__(self):
        return 'Title: ' + self.title + ' / Url: ' + str(self.url)

    def toJson(self):
        return {'title': self.title, 'url': self.url}

