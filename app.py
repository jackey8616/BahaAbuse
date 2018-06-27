import requests
from sanic import Sanic
from sanic.response import json

from crawler import Crawler

app = Sanic(__name__)
crawler = Crawler('https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18')

@app.route('/')
async def index(request):
    return json({"hello": "world"})

if __name__ == '__main__':
    crawler.crawl()
    app.run()
    
