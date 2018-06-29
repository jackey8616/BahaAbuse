import re, requests, jieba
from html.parser import HTMLParser
from simhash import Simhash

class Content(object):

    def __init__(self, article):
        if article:
            self.article = article
            self.header = None
            self.body = None

    def crawlContent(self, detail):
        response = requests.get('https://forum.gamer.com.tw/{}?bsn={}&snA={}'.format(detail['php'], detail['bsn'], detail['snA']))
        html = re.search('<div id=\"BH-master\">.*?<div id=\"BH-slave\">', response.text, flags=re.DOTALL).group()
        header = re.search('c-post__header.*?c-post__body', html, flags=re.DOTALL).group()
        body = re.search('c-post__body.*?c-post__footer', html, flags=re.DOTALL).group()
        self.header = str(header[header.find('>') + 1:header.rfind('<div')]),
        self.body = { 
            'html': str(body[body.find('<div') - 1:body.rfind('</article')]),
            'simhash': None
        }

    def htmlFilte(self):
        parser = HTMLParser()
        bodyArticle = parser.unescape(re.sub('<.*?>', "", self.body['html'], flags=re.DOTALL))
        wordFilte = jieba.cut(bodyArticle, cut_all=False) 
        simhash = Simhash(wordFilte, f=32).value
        self.body['simhash'] = simhash

    def __str__(self):
        return 'Html: ' + str(self.html)

    def toJson(self):
        if self.header and self.body:
            return {
                'header': self.header,
                'body': {
                    'html': self.body['html'],
                    'simhash': self.body['simhash'] 
                } 
            }
        else:
            return { 'header': str(None), 'body': str(None) }

    @staticmethod
    def fromJson(doc):
        content = Content(None)
        content.header = doc['header']
        if doc['body'] != 'None':
            content.body = {
                'html': doc['body']['html'],
                'simhash': doc['body']['simhash']
            }
        else:
            content.body = None
        return content
            

