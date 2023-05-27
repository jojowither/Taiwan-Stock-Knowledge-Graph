examples = """
# 查詢股票代碼2330基本資訊
MATCH (m:Stock{code:'2330'}) 
RETURN m
# Concept(概念股)種類的總數
MATCH (n:Concept) 
RETURN count(distinct(n))
# 股票代碼2330有多少副總經理在其他公司也是董監事經理人或大股東
MATCH (m:Stock{code:'2330'})<-[:employ_of{jobs:'副總經理'}]-(n:Person)-[e2:employ_of]->(q:Stock)
RETURN n, e2
# 台積電有哪些獨立董事
MATCH (m:Stock{name:'台積電'})<-[:employ_of{jobs:'獨立董事'}]-(n:Person)
RETURN n
# 有哪些'電腦及週邊設備業'也是'AI概念股'
MATCH (:Concept{name:'AI人工智慧'})<-[:concept_of]-(m:Stock)-[:industry_of]->(:Industry{name:'電腦及週邊設備業'})
RETURN m
# 列出仁寶所有零持股的副總經理
MATCH (:Stock{name:'仁寶'})<-[:employ_of{jobs:'副總經理', stock_num:0}]-(p1:Person)
RETURN p1
# 列出仁寶副總經理持股張數的基本統計
MATCH (:Stock{name:'仁寶'})<-[emp:employ_of{jobs:'副總經理'}]-(p1:Person)
WITH emp.stock_num AS num
RETURN min(num) AS min, max(num) AS max, avg(num) AS avg_characters, stdev(num) AS stdev
# 仁寶副總經理有多少比例零持股
MATCH (:Stock{name:'仁寶'})<-[:employ_of{jobs:'副總經理', stock_num:0}]-(p1:Person)
MATCH (:Stock{name:'仁寶'})<-[:employ_of{jobs:'副總經理'}]-(p2:Person)
RETURN count(distinct(p1))*1.0/ count(distinct(p2)) as ratio
# 仁寶副總經理有多少比例持股小於1000
MATCH (:Stock{name:'仁寶'})<-[emp:employ_of{jobs:'副總經理'}]-(p1:Person)
MATCH (:Stock{name:'仁寶'})<-[:employ_of{jobs:'副總經理'}]-(p2:Person)
WHERE emp.stock_num < 1000
RETURN count(distinct(p1))*1.0/ count(distinct(p2)) as ratio
# 券商 美林 買超張數超過1000張的股票
MATCH (d:Dealer{name:'美林'})-[bs:buy_or_sell]->(s:Stock)
WHERE bs.amount>1000
RETURN s
# 股票代碼2330跟股票代碼2454在概念股上的最短路徑
MATCH (a:Stock {code:'2330'}), (b:Stock {code:'2454'})
MATCH p=allShortestPaths((a)-[:concept_of*]-(b))
WITH [node IN nodes(p) where node:Concept | node.name] AS concept
RETURN concept 
# 查詢含有最多degree(不考慮方向以及關聯類別)的前10個股票
MATCH (s:Stock)
RETURN s.name AS stock, apoc.node.degree(s) AS degree 
ORDER BY degree DESC LIMIT 10
# 查詢跟最多股票有關係的前35位董事
MATCH (p:Person)
RETURN p.name AS person, apoc.node.degree(p) AS degree 
ORDER BY degree DESC LIMIT 35
# 查詢總持股前35最多的董事
MATCH (p:Person)-[r:employ_of]-(:Stock)
RETURN p.name AS person, sum(r.stock_num) as stockNum
ORDER BY stockNum DESC LIMIT 35
"""