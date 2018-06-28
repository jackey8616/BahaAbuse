import re, requests
from datetime import timedelta

from .article import Article

class Script(object):

    def __init__(self, html):
        self.url = html[36:-11]
        self.name = self.url[self.url.rfind('/') + 1:].split('?')[0]

    def __str__(self):
        return 'Script ' + self.name + ' / Url: ' + self.url

class BPage(object):

    def __init__(self, collection, html, bsn):
        self.col = collection
        self.bsn = bsn

        self.headHtml = re.search('<head>.*?</head>', html, flags=re.DOTALL).group()
        self.bodyHtml = re.search('<body>.*?</body>', html, flags=re.DOTALL).group()

        self.boardName = re.search('<title>.*?</title>', html).group()[7:-19]

    def lastUpdateOffset(self):
        firstArticle = None
        secondArticle = None
        for each in range(0, len(self.articles)):
            if not self.articles[each].isSticky():
                if firstArticle == None:
                    firstArticle = self.articles[each]
                else:
                    secondArticle = self.articles[each]
                    break
        return firstArticle.timeOffset(secondArticle).total_seconds() if firstArticle and secondArticle else None

    def script(self):
        self.scripts = {}
        scripts = re.findall('<script type=\"text/javascript\" src=\".*?\"></script>', self.headHtml)
        for each in scripts:
            script = Script(each)
            self.scripts[script.name] = script
            #print(script)
        return len(self.scripts)

    def subboard(self):
        self.subboards = {}
        response = requests.get(self.scripts[str(self.bsn) + '.js'].url)
        subfunc = re.search('function subtitle\(subbsn\) \{.*\}', response.text, flags=re.DOTALL).group()
        arrays = re.findall('subtitlearr\[[0-9]+]\ = \'.*?\';', subfunc, flags=re.DOTALL)
        for each in arrays:
            index = int(each[12:each.find(']')])
            name = each[each.find('\'') + 1:-2]
            self.subboards[index] = name
            #print(index, name)
        return len(self.subboards)

    def articleList(self):
        self.articles = []
        self.articleListHtml = re.search('<table class=\"b-list\">.*</table>', self.bodyHtml, flags=re.DOTALL).group(0)
        articlesHtml = re.findall('<tr class=\"b-list__row.*?</tr>', self.articleListHtml, flags=re.DOTALL)
        for each in articlesHtml:
            article = Article(each)
            self.articles.append(article) 
            if self.col.find(article.keyJson()).count() == 0:
                insertRes = self.col.insert_one(article.toJson())
                print('  => [{}] Crawled new article need add or update: {}...'.format(insertRes.inserted_id, article.main.title[:25]))
        return len(self.articles)

