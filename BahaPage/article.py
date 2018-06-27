import re

class User(object):

    def __init__(self, html):
        self.user = re.search('>.*?</a>', html).group(0)[1:-4]
        self.url = re.search('href=\".*?\"', html).group(0)[6:-1]
    
    def __str__(self):
        return 'User: ' + self.user

class Summary(object):

    def __init__(self, html):
        summaryHtml = re.search('<td class=\"b-list__summary\">.*?</td>', html, flags=re.DOTALL).group(0)
        self.rowSticky = 'row--sticky' in html
        self.summaryId = int(re.search('data-subbsn=\".*?"', summaryHtml).group(0)[13:-1])
        if 'span' in summaryHtml:
            self.gp = int(re.search('>.*?</span>', summaryHtml).group(0)[1:-7])
        else:
            self.gp = 0

    def __str__(self):
        return ('[Sticky]' if self.rowSticky else '') + 'Summary: ' + str(self.summaryId) + ' / GP: ' + str(self.gp)

class Main(object):

    def __init__(self, html):
        mainHtml = re.search('<td class=\"b-list__main\">.*?</td>', html, flags=re.DOTALL).group(0)
        if 'href' in mainHtml:
            self.title = re.search('>.*?</a>', mainHtml).group(0)[1:-4]
            self.url = re.search('href=\".*?\"', mainHtml).group(0)[6:-1]
        else:
            self.title = re.search('>.*?</span>', mainHtml).group(0)[1:-7]
            self.url = None

    def __str__(self):
        return 'Title: ' + self.title + ' / Url: ' + str(self.url)

class Count(object):

    def __init__(self, html):
        countHtml = re.search('<td class=\"b-list__count\">.*?</td>', html, flags=re.DOTALL).group(0)
        reply = re.search('<p class=\"b-list__count__number\">.*?</p>', countHtml, flags=re.DOTALL).group(0)
        self.reply = int(reply.split('</span>/\n<span>')[0][40:])
        self.view = int(reply.split('</span>/\n<span>')[1][:-12])
        userHtml = re.search('<p class=\"b-list__count__user\">.*?</p>', countHtml, flags=re.DOTALL).group(0)
        self.user = User(userHtml)

    def __str__(self):
        return 'Reply: ' + str(self.reply) + ' / View: ' + str(self.view) + ' / Author: ' + self.user.user

class Time(object):

    def __init__(self, html):
        timeHtml = re.search('<td class=\"b-list__time\">.*?</td>', html, flags=re.DOTALL).group(0)
        self.replyTime = re.search('>.*</a>', timeHtml).group(0)[1:-4]
        userHtml = re.search('<p class=\"b-list__time__user\">.*?</p>', timeHtml, flags=re.DOTALL).group(0)
        self.user = User(userHtml)

    def __str__(self):
        return 'Last Reply Time: ' + self.replyTime + ' By: ' + self.user.user

class Article(object):

    def __init__(self, html):
        self.summary = Summary(html)
        self.main = Main(html)
        self.count = Count(html)
        self.time = Time(html)

    def __str__(self):
        return str(self.summary) + ' / ' + str(self.main) + ' / ' + str(self.count) + ' / ' + str(self.time)
        
