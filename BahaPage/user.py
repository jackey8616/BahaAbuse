import re

class User(object):

    def __init__(self, html):
        self.user = re.search('>.*?</a>', html).group(0)[1:-4]
        self.url = re.search('href=\".*?\"', html).group(0)[6:-1]
    
    def __str__(self):
        return 'User: ' + self.user

    def toJson(self):
        return {'user': self.user, 'url': self.url}

