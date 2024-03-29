# Taiwan Stock Knowledge Graph with ChatGPT

爬取公開資料集並使用Neo4j建構台灣股市的知識圖譜，並將此知識圖譜作為ChatGPT的知識庫。

公開資料集/相關股票套件有

- [twstock](https://github.com/mlouielu/twstock)
- [永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)
- [Pchome股市概念股](https://pchome.megatime.com.tw/group/sto3)

Welcome to watch, star or fork.

![](img/kg1.png)

![](img/NeoGPT_sample.png)

---

## 實體關聯定義

![](img/stock_kg_structure.png)

目前定義有六種實體：
- **Person**表示董監，從[永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)抽取出
- **Stock**所有證券的名字，代號，從[twstock](https://github.com/mlouielu/twstock)抽取出，屬性未來可能會加上股價、漲跌
- **StockType**表示股票、ETF、權證等等，從[twstock](https://github.com/mlouielu/twstock)抽取出
- **Industry**表示產業類別，如半導體業、航運業等等，從[twstock](https://github.com/mlouielu/twstock)抽取出
- **Concept**表示概念股，如台積電有多個概念股，如5G、APPLE概念股等等，從[Pchome股市概念股](https://pchome.megatime.com.tw/group/sto3)抽取出
- **Dealer**表示券商/主力得分點，如隔日沖券商 美林、元大-土城永寧、國票-敦北法人等等，從[永豐金證券-主力進出](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_7?ticker=)抽取出

五種關聯:
- **employ_of**表示董監/大股東跟該股票的關係，屬性有職位以及持股張數，從[永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)抽取出
- **type_of**表示該股票屬於何種類型
- **industry_of**表示該股票屬於何種行業
- **concept_of**表示該股票有哪些概念股
- **buy_or_sell**表示券商對該股票的買賣超，正值為買超，負值為賣超

查詢schema，啟動neo4j後
```cypher
CALL db.schema.visualization()
```
![](img/kg_schema.png)


---
## 套件安裝

### python套件安裝

```bash
pip install -r requirements.txt
```

### 在linux中使用selenium

1. install Chrome Binary

```bash
# Install Chrome.
sudo curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add
sudo echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
# Update our system
sudo apt-get -y update
# Install Chrome
sudo apt-get -y install google-chrome-stable
```

2. install Chrome Driver
```bash
# Install Chromedriver
wget -N https://chromedriver.storage.googleapis.com/112.0.5615.28/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
# Remove zip file
rm ~/chromedriver_linux64.zip
# Move driver to bin location
sudo mv -f ~/chromedriver /usr/local/bin/chromedriver
# Give it rights
sudo chown root:root /usr/local/bin/chromedriver
sudo chmod 0755 /usr/local/bin/chromedriver
```

上面 112.0.5615.28為driver版本，可以透過該網站選擇需求的driver版本

ref: https://stackoverflow.com/questions/68283578/how-can-i-run-selenium-on-linux

---

## 資料集建構

```bash
cd src
python get_stock_info.py
python get_executive.py
python get_concept_stock.py
python get_dealer.py
```


以上是建構初始資料集，Neo4j需要再針對以上資料集生成對應的格式，可以理解為上面實體關聯關係圖的所有實體關聯，我們都要為他們建立一個檔案，上面實體關聯總共有11種，所以要有11個檔案。對於格式要求可以參考 https://neo4j.com/docs/operations-manual/current/tutorial/neo4j-admin-import/


建立Neo4j可接受的格式：
```bash
cd src
python build_import_csv.py
```

檔案生成在`data/import`

---

## 使用Neo4j生成知識圖譜

### Installation
Version: Neo4j 4.2.2 

關於Neo4j的安裝啟動，建議直接從[官方文件1](https://neo4j.com/docs/operations-manual/current/)以及[官方文件2](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/#debian-installation)閱讀起 

這裡提供快速教學

進入 https://neo4j.com/download-center/  去選版本或是 直接點 https://neo4j.com/download-thanks/?edition=community&release=4.2.2&flavour=unix

接著解壓縮
```bash
tar -xf neo4j-community-4.2.2-unix.tar.gz
```
擷取出來的資料夾為`$NEO4J_HOME`

執行neo4j
```bash
cd $NEO4J_HOME/bin
./neo4j console
```

用Mac如果出現
Unable to find any JVMs matching version "11".
No Java runtime present, try --request to install.
參考 https://community.neo4j.com/t/unable-to-find-any-jvms-matching-version-11/18183/3

```bash
brew install openjdk@11
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

and then visit `http://localhost:7474`，接著更改預設密碼

### Linux remote setting

```bash
sudo vim /etc/neo4j/neo4j.conf
# 將這句註解拿掉 server.default_listen_address=0.0.0.0
```

ref: https://neo4j.com/docs/operations-manual/current/configuration/file-locations/

### Neo4j Graph Data Science (GDS) 

安裝圖演算法套件

參考 https://neo4j.com/docs/graph-data-science/current/installation/


### Neo4j APOC 安裝

#### APOC Core

APOC Core can be installed by moving the APOC jar file from the `$NEO4J_HOME/labs` directory to the `$NEO4J_HOME/plugins` directory and restarting Neo4j.

若`$NEO4J_HOME/labs`沒檔案，可以用下載的方式，如下

```bash
sudo curl https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/5.6.0/apoc-5.6.0-extended.jar -o /var/lib/neo4j/plugins/apoc-5.6.0-extended.jar -L
sudo curl https://github.com/neo4j/apoc/releases/download/5.6.0/apoc-5.6.0-core.jar -o /var/lib/neo4j/plugins/apoc-5.6.0-core.jar -L
sudo neo4j restart
```

若做完以上流程進到cypher shell無法執行`call apoc.help('apoc')`，可以調整`/etc/neo4j/neo4j.conf`檔案

```bash
sudo vim /etc/neo4j/neo4j.conf
```

註解掉並添加`dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,gds.*,apoc.*`

以及註解掉並添加`dbms.security.procedures.unrestricted=apoc.*`

ref
- https://neo4j.com/labs/apoc/4.4/installation/ 
- https://stackoverflow.com/questions/42740355/how-to-install-apoc-for-neo4j



---

### 生成圖譜

```bash
cd data/
sudo neo4j-admin database import full --nodes=import/person.csv --nodes=import/stock.csv --nodes=import/stock_type.csv --nodes=import/concept.csv --nodes=import/industry.csv --nodes=import/dealer.csv --relationships=import/person_stock.csv --relationships=import/stock_industry.csv --relationships=import/stock_concept.csv --relationships=import/stock_st.csv --relationships=import/dealer_stock.csv --overwrite-destination=true neo4j
```

最後面`neo4j`為預設資料庫的名字

目前上傳的資料集差不多是在2023/4/17前後的資訊，如果需要最新資訊可以回到[資料集建構](##資料集建構)，去爬下最新的資料。

**注意**，若使用community版本import資料失敗，可去`/var/lib/neo4j/data/databases`和`/var/lib/neo4j/data/transactions`中刪除欲創建的資料庫，此例資料庫名稱為`neo4j`，刪除成功後再重新執行上面指令。

**注意2**，若資料import成功但browser無法正確顯示資訊，則重啟neo4j試試，`sudo neo4j restart`

---

## 使用Cypher於知識圖譜回答問題


套件需求
```bash
pip install python-igraph
pip install py2neo
```

### 問題

1. GG有多少副總在其他公司也是董監事經理人或大股東
1. GG有多少獨立董事
1. 有多少'電腦及週邊設備業'也是'AI概念股'
1. 列出寶寶所有零持股的副總
1. 寶寶副總有多少比例零持股
1. 寶寶副總有多少比例持股小於1000
1. 查詢跟最多股票有關係的前35位董事
1. 隔日沖券商 美林 買超張數超過1000張的股票

...等等

詳細請查看 `src/cypher_script.ipynb`

---

## Web Application

![](img/kg4.png)

- Application Type: Python-Web Application
- Web framework: Flask (Micro-Webframework)
- Neo4j Database Connector: Neo4j Python Driver for Cypher Docs
- Database: Neo4j-Server (4.x)
- Frontend: jquery, bootstrap, d3.js

### Run locally
```bash
cd web/
uvicorn run:app --reload --host 0.0.0.0
```



---

## 自定義視覺化
[neovis](https://github.com/neo4j-contrib/neovis.js)

執行neo4j後
```bash
cd $NEO4J_HOME/bin
./neo4j console
```

開啟`cus_vis.html`，記得把config改成自己的帳號密碼

這裡自定義的視覺化為使用graph algorithms，只畫出股票及董事之間的關係。
```bash
python run_graph_algo.py
```

Stock size為Stock與概念股的pagerank，color為Stock與概念股的community detection

Person size為Person與Stock的pagerank，color為Person與Stock的community detection

employ_of粗細為該董監持股數除以全部董監持股數

![](img/kg2.png)
![](img/kg3.png)

---

## ChatGPT

整體流程如下

![](img/ChatBot_flow.png)

使用streamlit作為與ChatGPT對話的介面

首先須將`.env.example`內的參數改成自己的，並更名為`.env`

執行以下指令

```bash
# 確認neo4j有啟動
sudo neo4j restart
streamlit run main.py --server.address=0.0.0.0
```


此外，`chat_app/training.py`為作為ChatGPT學習neo4j的提示工程，若要達到更好的對話或查詢效果，除了更改openai model以外，也可以撰寫更完整的提示。


---

## Reference

- https://github.com/lemonhu/stock-knowledge-graph
- https://towardsdatascience.com/graph-analytics-with-py2neo-f629ba71051b
- https://github.com/neo4j-contrib/neovis.js
- https://medium.com/neo4j/graph-visualization-with-neo4j-using-neovis-js-a2ecaaa7c379
- https://www.lyonwj.com/blog/graph-of-thrones-neo4j-social-network-analysis
- https://stackoverflow.com/questions/23310114/how-to-reset-clear-delete-neo4j-database
- https://github.com/nicolewhite/neo4j-flask
- https://github.com/neo4j-examples/movies-python-bolt
- https://observablehq.com/@xianwu/force-directed-graph-network-graph-with-arrowheads-and-lab
- https://medium.com/neo4j/context-aware-knowledge-graph-chatbot-with-gpt-4-and-neo4j-d3a99e8ae21e

