import re

from .user import User

class Count(object):

    def __init__(self, article, html):
        if article and html:
            self.arcticle = article
            countHtml = re.search('<td class=\"b-list__count\">.*?</td>', html, flags=re.DOTALL).group(0)
            reply = re.search('<p class=\"b-list__count__number\">.*?</p>', countHtml, flags=re.DOTALL).group(0)
            self.reply = int(reply.split('</span>/\n<span>')[0][40:])
            self.view = int(reply.split('</span>/\n<span>')[1][:-12])
            userHtml = re.search('<p class=\"b-list__count__user\">.*?</p>', countHtml, flags=re.DOTALL).group(0)
            self.user = User(userHtml)

    def __str__(self):
        return 'Reply: ' + str(self.reply) + ' / View: ' + str(self.view) + ' / Author: ' + self.user.user

    def toJson(self):
        return {'reply': self.reply, 'view': self.view, 'user': self.user.toJson()}

    def keyJson(self):
        return {'reply': self.reply}

    @staticmethod
    def fromJson(doc):
        count = Count(None, None)
        count.reply = doc['reply']
        count.view = doc['view']
        count.user = User.fromJson(doc['user'])
        return count

