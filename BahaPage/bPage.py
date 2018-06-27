import re

from .article import Article

class Script(object):

    def __init__(self, html):
        self.url = html[36:-11]

    def __str__(self):
        return 'Script ' + self.url

class BPage(object):

    def __init__(self, html):
        self.headHtml = re.search('<head>.*?</head>', html, flags=re.DOTALL).group()
        self.bodyHtml = re.search('<body>.*?</body>', html, flags=re.DOTALL).group()

        self.scripts = []
        self.articles = []

        self.script()
        self.articleList()

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
            self.articles.append(article) 
            print(article)

