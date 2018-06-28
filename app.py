from pymongo import MongoClient
from bson.objectid import ObjectId
from sanic import Sanic
from sanic.response import json
from sanic_cors import CORS, cross_origin

from crawler import Crawler
from BahaPage.article import Article

mongo = MongoClient('mongodb://localhost:27017/')
db = mongo['BahaAbuse']
app = Sanic(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
crawler = Crawler(db, 'Minecraft', 'https://forum.gamer.com.tw/B.php?bsn=18673&subbsn=0', 18673)

@app.route('/')
async def index(request):
    return json({"hello": "world"})

@app.route('/api/article-list')
async def articleList(request):
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

@app.route('/api/article')
async def article(request):
    query = {}
    res = {'subboards': {}, 'article': []}
    for index, val in crawler.bPage.subboards.items():
        res['subboards'][index] = val
    for key, val in request.raw_args.items():
        query['detail.' + key] = int(val) if key != 'php' else val
    res['article'] = db.Minecraft.find_one(query)
    if res['article']['content']['html'] == 'None':
        print('Crawling content...')
        art = Article.fromJson(res['article'])
        art.crawlContent()
        db.Minecraft.update(query, {"$set": {"content": art.content.toJson()}}, upsert=False)
        res['article'].update(art.toJson())
        res['article'] = art.toJson()
    return json({'response': res})

if __name__ == '__main__':
    crawler.start()
    app.run()
    crawler.stopped.set()
    
