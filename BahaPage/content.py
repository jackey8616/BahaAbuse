import re, requests

class Content(object):

    def __init__(self, article):
        if article:
            self.article = article
            self.html = None

    def crawlContent(self, detail):
        response = requests.get('https://forum.gamer.com.tw/{}?bsn={}&snA={}'.format(detail['php'], detail['bsn'], detail['snA']))
        html = re.search('<div id=\"BH-master\">.*?<div id=\"BH-slave\">', response.text, flags=re.DOTALL).group()
        header = re.search('c-post__header.*?c-post__body', html, flags=re.DOTALL).group()
        body = re.search('c-post__body.*?c-post__footer', html, flags=re.DOTALL).group()
        self.html = {
            'header': header[header.find('>') + 1:header.rfind('<div')],
            'body': body[body.find('<div') - 1:body.rfind('</article')]
        }

    def __str__(self):
        return 'Html: ' + str(self.html)

    def toJson(self):
        if self.html:
            return { 'html': { 'header': self.html['header'], 'body': self.html['body'] } }
        else:
            return { 'html': str(None) }

    @staticmethod
    def fromJson(doc):
        content = Content(None)
        content.html = doc['content'] if 'content' in doc else None
        return content
            

