import os
from dotenv import load_dotenv
from py2neo import Graph

load_dotenv()

host = os.getenv('NEO4J_URL')
user = os.getenv('NEO4J_USER')
password = os.getenv('NEO4J_PASS')
graph = Graph(host, password=password)


def run_query(query):
    results = graph.run(query).data()
    return results


if __name__ == '__main__':
    print(run_query("""
    match (m:Stock{code:'2330'}) return m
    """))