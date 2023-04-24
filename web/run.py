import os
from json import dumps
import logging
from logging import FileHandler

from fastapi import FastAPI, Response, Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


import uvicorn
from py2neo import Graph


templates = Jinja2Templates(directory="static")
app = APIRouter()

url = 'bolt://127.0.0.1:7687'
password = 'neo4jneo4j'
graph = Graph(url, password=password)


def serialize_exec(executive):
    return {
        'name': executive.start_node['name'],
        'jobs': executive['jobs'],
        'stock_num': executive['stock_num']
    }


@app.get("/")
async def home(request: Request):
	return templates.TemplateResponse("index.html",{"request":request})



@app.get("/search")
async def get_search(q: str):
    query = f'''
            MATCH (c:Concept)<-[:concept_of]-(s:Stock{{code:'{q}'}})-[:industry_of]->(i:Industry)
            RETURN s, i, c
            '''
    results = graph.run(query).data()

    return Response(dumps({"stock_code": results[0]['s']['code'],
                            "stock_name": results[0]['s']['name'],
                            "industry": results[0]['i']['name'],
                            "concept": ', '.join([result['c']['name'] for result in results])}),
                    media_type="application/json")


@app.get("/executive/{stock}")
async def get_executive(stock: str):
    query = f'''
            MATCH (m:Stock{{code:'{stock}'}})<-[r:employ_of]-(n:Person)
            RETURN n, r
            '''

    results = graph.run(query).data()

    return Response(dumps({"stock_code": stock,
                           "stock_name": results[0]['r'].end_node['name'],
                           "executive": [serialize_exec(result['r']) for result in results]}),
                    media_type="application/json")


## 希望跟查詢連動，跳出來的是，查詢股票的所有董事、概念股、產業別、以及買賣分點
## 改回傳格式
## node: id, name, lable(entity type), pageranke(todo)
## link: source, target, type
@app.get("/graph")
async def get_graph(q: str):
    query = f'''
            MATCH (s:Stock{{code:'{q}'}}) 
            MATCH p=(s)-[rels]-(others)
            RETURN s, rels, others
            '''
    results = graph.run(query).data()

    nodes = []
    rels = []
    _id = 1
    nodes.append({"id": 0,
                "name": results[0]['s']['name'], 
                "label": set(results[0]['s'].labels).pop()})

    for result in results:
        nodes.append({"id": _id,
                    "name": result['others']['name'], 
                    "label": set(result['others'].labels).pop()})
        rels.append({"source": 0, 
                    "target": _id,
                    "type":type(result['rels']).__name__})
        _id += 1


    return Response(dumps({"nodes": nodes, "links": rels}),
                    media_type="application/json")

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0")
