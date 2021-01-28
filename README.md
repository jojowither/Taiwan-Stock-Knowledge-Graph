# Taiwan Stock Knowledge Graph

爬取公開資料集並使用Neo4j建構台灣股市的知識圖譜

公開資料集/相關股票套件有

- [twstock](https://github.com/mlouielu/twstock)
- [永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)
- [Pchome股市概念股](https://pchome.megatime.com.tw/group/sto3)

Welcome to watch, star or fork.

![](kg1.png)

---

## 實體關聯定義

![](stock_kg_structure.png)

目前定義有五種實體：
- **Person**表示董監，從[永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)抽取出
- **Stock**所有證券的名字，代號，從[twstock](https://github.com/mlouielu/twstock)抽取出，屬性未來可能會加上股價、漲跌
- **StockType**表示股票、ETF、權證等等，從[twstock](https://github.com/mlouielu/twstock)抽取出
- **Industry**表示產業類別，如半導體業、航運業等等，從[twstock](https://github.com/mlouielu/twstock)抽取出
- **Concept**表示概念股，如台積電有多個概念股，如5G、APPLE概念股等等，從[Pchome股市概念股](https://pchome.megatime.com.tw/group/sto3)抽取出

四種關聯:
- **employ_of**表示董監/大股東跟該股票的關係，屬性有職位以及持股張數，從[永豐金證券-董監持股](https://www.sinotrade.com.tw/Stock/Stock_3_1/Stock_3_1_6_2?ticker=)抽取出
- **type_of**表示該股票屬於何種類型
- **industry_of**表示該股票屬於何種行業
- **concept_of**表示該股票有哪些概念股


---

## 資料集建構

```bash
cd src
python get_stock_info.py
python get_executive.py
python get_concept_stock.py
```


以上三句是建構初始資料集，Neo4j需要再針對以上資料集生成對應的格式，可以理解為上面實體關聯關係圖的所有實體關聯，我們都要為他們建立一個檔案，上面實體關聯總共有9種，所以要有9個檔案。對於格式要求可以參考 https://neo4j.com/docs/operations-manual/current/tutorial/neo4j-admin-import/


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

關於Neo4j的安裝啟動，建議直接從[官方文件](https://neo4j.com/docs/operations-manual/current/)閱讀起 

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

我是用Mac，如果出現
Unable to find any JVMs matching version "11".
No Java runtime present, try --request to install.
參考 https://community.neo4j.com/t/unable-to-find-any-jvms-matching-version-11/18183/3

```bash
brew install openjdk@11
sudo ln -sfn /usr/local/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

and then visit `http://localhost:7474`，接著更改預設密碼


### Neo4j Graph Data Science (GDS) 

安裝圖演算法套件

參考 https://neo4j.com/docs/graph-data-science/current/installation/

---

### 生成圖譜

```bash
cd $NEO4J_HOME/bin
./neo4j-admin import --id-type=STRING --database=mydatabase --nodes stock/person.csv --nodes tock/stock.csv --nodes stock/stock_type.csv --nodes stock/concept.csv --nodes stock/industry.csv --relationships stock/person_stock.csv --relationships stock/stock_industry.csv --relationships stock/stock_concept.csv --relationships stock/stock_st.csv
```

`mydatabase`為我自己命名資料庫的名字，可以更改

**注意**，把`data/import`整個資料夾放到`$NEO4J_HOME/bin`裡，我自己是有再將資料夾重新命名為`stock`

---

## 使用Cypher於知識圖譜回答問題
查看 `src/test.ipynb`