import re

class Summary(object):

    def __init__(self, article, html):
        self.article = article
        summaryHtml = re.search('<td class=\"b-list__summary\">.*?</td>', html, flags=re.DOTALL).group(0)
        self.rowSticky = 'row--sticky' in html
        self.summaryId = int(re.search('data-subbsn=\".*?"', summaryHtml).group(0)[13:-1])
        if 'span' in summaryHtml:
            self.gp = int(re.search('>.*?</span>', summaryHtml).group(0)[1:-7])
        else:
            self.gp = 0

    def __str__(self):
        return ('[Sticky]' if self.rowSticky else '') + 'Summary: ' + str(self.summaryId) + ' / GP: ' + str(self.gp)

    def toJson(self):
        return {'rowSticky': self.rowSticky, 'summaryId': self.summaryId, 'gp': self.gp }

