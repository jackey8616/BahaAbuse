import re
from datetime import timedelta

from .article import Article

class Script(object):

    def __init__(self, html):
        self.url = html[36:-11]

    def __str__(self):
        return 'Script ' + self.url

class BPage(object):

    def __init__(self, collection, html):
        self.col = collection

        self.headHtml = re.search('<head>.*?</head>', html, flags=re.DOTALL).group()
        self.bodyHtml = re.search('<body>.*?</body>', html, flags=re.DOTALL).group()

        self.boardName = re.search('<title>.*?</title>', html).group()[7:-19]
        self.scripts = []
        self.articles = []

        self.script()
        self.articleList()

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
        scripts = re.findall('<script type=\"text/javascript\" src=\".*?\"></script>', self.headHtml)
        for each in scripts:
            script = Script(each)
            self.scripts.append(script)
            #print(script)

    def articleList(self):
        self.articleListHtml = re.search('<table class=\"b-list\">.*</table>', self.bodyHtml, flags=re.DOTALL).group(0)
        articlesHtml = re.findall('<tr class=\"b-list__row.*?</tr>', self.articleListHtml, flags=re.DOTALL)
        for each in articlesHtml:
            article = Article(each)
            if self.col.find(article.keyJson()).count() == 0:
                self.articles.append(article) 
                insertRes = self.col.insert_one(article.toJson())
                print('  => [{}] Crawled new article need add or update: {}...'.format(insertRes.inserted_id, article.main.title[:25]))

