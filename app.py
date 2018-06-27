from pymongo import MongoClient
from sanic import Sanic
from sanic.response import json

from crawler import Crawler

mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['BahaAbuse']
app = Sanic(__name__)
crawler = Crawler(db, 'Minecraft', 'https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=18')

@app.route('/')
async def index(request):
    return json({"hello": "world"})

if __name__ == '__main__':
    crawler.start()
    app.run()
    crawler.stopped.set()
    
