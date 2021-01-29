import time
from collections import defaultdict

from igraph import Graph as IGraph
from py2neo import Graph

URL = 'bolt://localhost:7687'
USER = "neo4j" # Default by neo4j
PASSWORD = 'jojo'


def time_count_wrapper(func):
    def time_count():
        ts = time.time()
        func()
        te = time.time()
        print(f"Time consume: {te-ts:.3f} s")
    return time_count


def connectToNeo4j(user, password):
    '''
    Establishes a connection with neo4j.
    Default neo4j username is 'neo4j'
    '''
    connection = Graph(URL, user=user, password=password)
    return connection


def removeExistingData(connection):
    '''
    Neo4j does not replace a dataset when additional data is added, that is
    why we need to remove all existing data before loading the dataset again
    '''
    connection.run("MATCH (n) DETACH DELETE n")


# PageRank: The size of each node is proportional to the number and size of the other nodes pointing to it in the network. 
def pageRank(connection, ig, query):
    pg = ig.pagerank()
    pgvs = []
    for p in zip(ig.vs, pg):
        pgvs.append({"name": p[0]["name"], "pg": p[1]})
    connection.run(query, nodes=pgvs)


def communityDetection(connection, ig, query, step=3):

    clusters = IGraph.community_walktrap(ig, steps=step).as_clustering()

    nodes = [{"name": node["name"]} for node in ig.vs]
    for node in nodes:
        idx = ig.vs.find(name=node["name"]).index
        node["community"] = clusters.membership[idx]
    connection.run(query, nodes=nodes)


def get_rel_thickness(connection):
    write_stock_weight_query = '''
    MATCH (p:Person)-[r:employ_of]->(s:Stock)
    RETURN p.name as person_name, r.stock_num as stock_num, s.name as stock_name
    '''

    data = connection.run(write_stock_weight_query).data()
    
    total_stock_nums = defaultdict(int)
    for person in data:
        total_stock_nums[person['stock_name']] += person['stock_num']
    for person in data:
        person['stock_ratio'] = person['stock_num']/total_stock_nums[person['stock_name']]

    ## Person和Stock關聯employ_of線的粗細，用股東總持股當分母，董事持股數當分子
    write_stock_weight_query = '''
    UNWIND $nodes AS n
    MATCH (p:Person)-[r:employ_of]->(s:Stock)
    WHERE p.name = n.person_name AND s.name = n.stock_name
    SET r.stock_ratio = n.stock_ratio
    '''
    connection.run(write_stock_weight_query, nodes=data)



def main():
    connection = connectToNeo4j(USER, PASSWORD)

    # 選取所有股票與其概念股
    query = '''
    MATCH (s:Stock)-[r:concept_of]->(c:Concept)
    RETURN s.name, c.name
    '''
    ig = IGraph.TupleList(connection.run(query), weights=True)

    pageRank_query = '''
    UNWIND $nodes AS n
    MATCH (s:Stock) WHERE s.name = n.name
    SET s.pagerank = n.pg
    '''
    print('===Run Page Rank===')
    pageRank(connection, ig, pageRank_query)
    print('===Page Rank Done===\n')

    communityDetection_query = '''
    UNWIND $nodes AS n
    MATCH (s:Stock) WHERE s.name = n.name
    SET s.community = toInteger(n.community)
    '''
    print('===Run Community Detection===')
    communityDetection(connection, ig, query, step=3)
    print('===Community Detection Done===\n')


    # 選取所有股票與其董事
    query = '''
    MATCH (p:Person)-[r:employ_of]->(s:Stock)
    RETURN p.name, s.name
    '''
    ig = IGraph.TupleList(connection.run(query), weights=True)

    pageRank_query = '''
    UNWIND $nodes AS n
    MATCH (p:Person) WHERE p.name = n.name
    SET p.pagerank = n.pg
    '''
    print('===Run Page Rank===')
    pageRank(connection, ig, pageRank_query)
    print('===Page Rank Done===\n')

    communityDetection_query = '''
    UNWIND $nodes AS n
    MATCH (p:Person) WHERE p.name = n.name
    SET p.community = toInteger(n.community)
    '''
    print('===Run Community Detection===')
    communityDetection(connection, ig, query, step=2)
    print('===Community Detection Done===')

    # edge 粗細
    print('===Run Edge Thickness===')
    get_rel_thickness(connection)
    print('===Done===')


if __name__=='__main__':
    main()
