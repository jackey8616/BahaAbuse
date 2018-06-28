import re
from datetime import datetime, timedelta

from .user import User

class Time(object):

    def __init__(self, article, html):
        self.article = article
        timeHtml = re.search('<td class=\"b-list__time\">.*?</td>', html, flags=re.DOTALL).group(0)
        self.replyTime = self.timePreprocess(re.search('>.*</a>', timeHtml).group(0)[1:-4])
        userHtml = re.search('<p class=\"b-list__time__user\">.*?</p>', timeHtml, flags=re.DOTALL).group(0)
        self.user = User(userHtml)

    def timePreprocess(self, timeStr):
        time = datetime.today()
        if len(timeStr) == 11:
            date = timeStr.split(' ')[0].split('/')
            time = time.replace(month=int(date[0]), day=int(date[1]))
        else:
            dayMinus = 0 if '今日' in timeStr else 1
            time -= timedelta(days=dayMinus)
        hourMin = timeStr.split(' ')[1].split(':')
        time = time.replace(hour=int(hourMin[0]), minute=int(hourMin[1]), second=0, microsecond=0) 
        return time

    def __str__(self):
        return 'Last Reply Time: ' + datetime.strftime(self.replyTime, '%Y-%m-%d %H:%M:%S') + ' By: ' + self.user.user

    def toJson(self):
        return {'replyTime': self.replyTime, 'user': self.user.toJson()}

