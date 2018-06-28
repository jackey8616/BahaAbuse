from pymongo import MongoClient
from bson.objectid import ObjectId
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin

from crawler import Crawler

mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['BahaAbuse']
app = Sanic(__name__)

crawler = Crawler(db, 'Minecraft', 'https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=0', 18673)

@app.route('/')
async def index(request):
    return json({"hello": "world"})

@app.route('/article')
@cross_origin(app)
async def article(request):
    query = request.raw_args
    res = {'subboards': {}, 'articles': []}
    #if '_id' in query.keys():
    #    query['_id'] = ObjectId(query['_id'])
    #cursor = db.Minecraft.find(query).limit(30)
    #for doc in cursor:
    #    doc['_id'] = str(doc['_id'])
    #    res.append(doc)
    for index, val in crawler.bPage.subboards.items():
        res['subboards'][index] = val
    for each in crawler.bPage.articles:
        res['articles'].append(each.toJson())
    return json({'response': res})

if __name__ == '__main__':
    crawler.start()
    app.run()
    crawler.stopped.set()
    
