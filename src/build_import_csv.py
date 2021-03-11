import csv
import hashlib
import os
from pathlib import Path
import twstock


def get_md5(string):
    """
    Get md5 according to the string
    """
    byte_string = string.encode("utf-8")
    md5 = hashlib.md5()
    md5.update(byte_string)
    result = md5.hexdigest()
    return result


def build_person(executive_prep, person_import):
    """
    Create an 'person' file in csv format that can be imported into Neo4j.
    format -> person_id:ID,name,:LABEL
    label -> Person
    """
    print(f'Writing to {person_import.name} file...')
    with open(executive_prep, 'r', encoding='utf-8') as file_prep, \
            open(person_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['person_id:ID', 'name', ':LABEL']
        file_import_csv.writerow(headers)
        person_set = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            person_set.add(row[0])
        for person in person_set:
            # generate md5 according to 'name'
            person_id = get_md5(person)
            info = [person_id, person, 'Person']
            file_import_csv.writerow(info)
    print('- done.')


def build_stock(stock_prep, stock_import):
    """
    Create an 'stock' file in csv format that can be imported into Neo4j.
    format -> company_id:ID,name,code,:LABEL
    label -> Stock
    """
    print(f'Writing to {stock_import.name} file...')

    with open(stock_prep, 'r', encoding='utf-8') as file_prep,\
            open(stock_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['stock_id:ID', 'name', 'code', 'market', ':LABEL']
        file_import_csv.writerow(headers)
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            info = [row[0], row[2], row[0], row[4], 'Stock']
            file_import_csv.writerow(info)
    print('- done.')


def build_stock_type(stock_prep, stock_type_import):
    """
    Create an 'stock_type' file in csv format that can be imported into Neo4j.
    format -> stocktype_id:ID,name,:LABEL
    label -> StockType
    """
    print(f'Writing to {stock_type_import.name} file...')
    with open(stock_prep, 'r', encoding='utf-8') as file_prep,\
            open(stock_type_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['stocktype_id:ID', 'name', ':LABEL']
        file_import_csv.writerow(headers)
        stock_types = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            stock_types.add(row[1])
        for stock_type in stock_types:
            stock_type_id = get_md5(stock_type)
            info = [stock_type_id, stock_type, 'StockType']
            file_import_csv.writerow(info)
    print('- done.')


def build_industry(stock_prep, industry_import):
    """
    Create an 'industry' file in csv format that can be imported into Neo4j.
    format -> industry_id:ID,name,:LABEL
    label -> Industry
    """
    print(f'Writing to {industry_import.name} file...')
    with open(stock_prep, 'r', encoding='utf-8') as file_prep,\
            open(industry_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['industry_id:ID', 'name', ':LABEL']
        file_import_csv.writerow(headers)
        industries = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            industry = row[3] if row[3] != '' else '無'
            industries.add(industry)
        for industry in industries:
            industry_id = get_md5(industry)
            info = [industry_id, industry, 'Industry']
            file_import_csv.writerow(info)
    print('- done.')


def build_concept(concept_prep, concept_import):
    """
    Create an 'concept' file in csv format that can be imported into Neo4j.
    format -> concept_id:ID,name,:LABEL
    label -> Concept
    """
    print(f'Writing to {concept_import.name} file...')
    with open(concept_prep, 'r', encoding='utf-8') as file_prep,\
            open(concept_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['concept_id:ID', 'name', ':LABEL']
        file_import_csv.writerow(headers)
        concepts = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            concept = row[0]
            concepts.add(concept)
        for concept in concepts:
            concept_id = get_md5(concept)
            info = [concept_id, concept, 'Concept']
            file_import_csv.writerow(info)
    print('- done.')


def bulid_dealer(dealer_prep, dealer_import):
    """
    Create an 'dealer' file in csv format that can be imported into Neo4j.
    format -> dealer_id:ID,name,:LABEL
    label -> Dealer
    """
    print(f'Writing to {dealer_prep.name} file...')
    with open(dealer_prep, 'r', encoding='utf-8') as file_prep, \
            open(dealer_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')

        headers = ['dealer_id:ID', 'name', ':LABEL']
        file_import_csv.writerow(headers)
        dealers = set()
        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            dealers.add(row[0])
        for dealer in dealers:
            # generate md5 according to 'name'
            dealer_id = get_md5(dealer)
            info = [dealer_id, dealer, 'Dealer']
            file_import_csv.writerow(info)
    print('- done.')


def build_person_stock(executive_prep, relation_import):
    """Create an 'person_stock' file in csv format that can be imported into Neo4j.
    format -> :START_ID,job,stock_num,:END_ID,:TYPE
               person                  stock
    type -> employ_of
    """
    print(f'Writing to {relation_import.name} file...')
    with open(executive_prep, 'r', encoding='utf-8') as file_prep, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', 'jobs', 'stock_num:int', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            start_id = get_md5(row[0])
            end_id = row[1]  # code
            relation = [start_id, row[2], row[3], end_id, 'employ_of']
            file_import_csv.writerow(relation)
    print('- done.')


# build stock and stock_type
def build_stock_st(stock_prep, relation_import):
    """Create an 'stock_st' file in csv format that can be imported into Neo4j.
    format -> :START_ID,:END_ID,:TYPE
               stock     stock_type
    type -> type_of
    """
    print(f'Writing to {relation_import.name} file...')
    with open(stock_prep, 'r', encoding='utf-8') as file_prep, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            start_id = row[0]  # code
            end_id = get_md5(row[1])
            relation = [start_id, end_id, 'type_of']
            file_import_csv.writerow(relation)
    print('- done.')


def build_stock_industry(stock_prep, relation_import):
    """Create an 'stock_industry' file in csv format that can be imported into Neo4j.
    format -> :START_ID,:END_ID,:TYPE
               stock     industry
    type -> industry_of
    """
    print(f'Writing to {relation_import.name} file...')
    with open(stock_prep, 'r', encoding='utf-8') as file_prep, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            start_id = row[0]  # code
            industry = row[3] if row[3] != '' else '無'
            end_id = get_md5(industry)
            relation = [start_id, end_id, 'industry_of']
            file_import_csv.writerow(relation)
    print('- done.')


def build_stock_concept(concept_prep, relation_import):
    """Create an 'stock_concept' file in csv format that can be imported into Neo4j.
    format -> :START_ID,:END_ID,:TYPE
               stock     concept
    type -> concept_of
    """
    print(f'Writing to {relation_import.name} file...')
    with open(concept_prep, 'r', encoding='utf-8') as file_prep, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            start_id = row[1]
            concept = row[0]
            end_id = get_md5(concept)

            # Maybe the twstock didn't update the new stcok
            if start_id not in twstock.codes:
                continue

            relation = [start_id, end_id, 'concept_of']
            file_import_csv.writerow(relation)
    print('- done.')


def build_dealer_stock(executive_prep, relation_import):
    """Create an 'dealer_stock' file in csv format that can be imported into Neo4j.
    format -> :START_ID,amount,:END_ID,:TYPE
               dealer           stock
    type -> buy_or_sell
    """
    print(f'Writing to {relation_import.name} file...')
    with open(executive_prep, 'r', encoding='utf-8') as file_prep, \
            open(relation_import, 'w', encoding='utf-8') as file_import:
        file_prep_csv = csv.reader(file_prep, delimiter=',')
        file_import_csv = csv.writer(file_import, delimiter=',')
        headers = [':START_ID', 'amount:int', ':END_ID', ':TYPE']
        file_import_csv.writerow(headers)

        for i, row in enumerate(file_prep_csv):
            if i == 0:
                continue
            start_id = get_md5(row[0])
            end_id = row[1]  # code
            relation = [start_id, row[2], end_id, 'buy_or_sell']
            file_import_csv.writerow(relation)
    print('- done.')


if __name__ == '__main__':
    prep_path = '../data/'
    import_path = '../data/import'
    if not os.path.exists(import_path):
        os.makedirs(import_path)

    # Node
    build_person(Path(prep_path)/'executive_prep.csv',
                 Path(import_path)/'person.csv')
    build_stock(Path(prep_path)/'tw_stock_info_prep.csv',
                Path(import_path)/'stock.csv')
    build_stock_type(Path(prep_path)/'tw_stock_info_prep.csv',
                     Path(import_path)/'stock_type.csv')
    build_industry(Path(prep_path)/'tw_stock_info_prep.csv',
                   Path(import_path)/'industry.csv')
    build_concept(Path(prep_path)/'concept_prep.csv',
                  Path(import_path)/'concept.csv')
    bulid_dealer(Path(prep_path)/'dealer_prep.csv',
                  Path(import_path)/'dealer.csv')

    # Relation
    build_person_stock(Path(prep_path)/'executive_prep.csv',
                       Path(import_path)/'person_stock.csv')
    build_stock_st(Path(prep_path)/'tw_stock_info_prep.csv',
                   Path(import_path)/'stock_st.csv')
    build_stock_industry(Path(prep_path)/'tw_stock_info_prep.csv',
                         Path(import_path)/'stock_industry.csv')
    build_stock_concept(Path(prep_path)/'concept_prep.csv',
                        Path(import_path)/'stock_concept.csv')
    build_dealer_stock(Path(prep_path)/'dealer_prep.csv',
                       Path(import_path)/'dealer_stock.csv')
    
