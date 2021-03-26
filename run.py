import os
from json import dumps
import logging
from logging import FileHandler

from flask import Flask, g, Response, request
from py2neo import Graph

app = Flask(__name__, static_url_path='/static/')

url = 'bolt://127.0.0.1:7687'
password = 'jojo'
graph = Graph(url, password=password)


def serialize_exec(executive):
    return {
        'name': executive.start_node['name'],
        'jobs': executive['jobs'],
        'stock_num': executive['stock_num']
    }


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        query = f'''
            MATCH (c:Concept)<-[:concept_of]-(s:Stock{{code:'{q}'}})-[:industry_of]->(i:Industry)
            RETURN s, i, c
            '''
        results = graph.run(query).data()

        return Response(dumps({"stock_code": results[0]['s']['code'],
                               "stock_name": results[0]['s']['name'],
                               "industry": results[0]['i']['name'],
                               "concept": ', '.join([result['c']['name'] for result in results])}),
                        mimetype="application/json")


@app.route("/executive/<stock>")
def get_executive(stock):
    query = f'''
            MATCH (m:Stock{{code:'{stock}'}})<-[r:employ_of]-(n:Person)
            RETURN n, r
            '''

    results = graph.run(query).data()

    return Response(dumps({"stock_code": stock,
                           "stock_name": results[0]['r'].end_node['name'],
                           "executive": [serialize_exec(result['r']) for result in results]}),
                    mimetype="application/json")


## TODO
# @app.route("/graph")
# def get_graph():


if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler('flask.log')
    app.logger.addHandler(handler)
    app.logger.info('Running the graph database at %s', url)
    app.run()
