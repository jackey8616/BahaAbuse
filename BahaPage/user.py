import re

class User(object):

    def __init__(self, html):
        if html:
            self.user = re.search('>.*?</a>', html).group(0)[1:-4]
            self.url = re.search('href=\".*?\"', html).group(0)[6:-1]
    
    def __str__(self):
        return 'User: ' + self.user

    def toJson(self):
        return {'user': self.user, 'url': self.url}
    
    @staticmethod
    def fromJson(doc):
        user = User(None)
        user.user = doc['user']
        user.url = doc['url']
        return user

