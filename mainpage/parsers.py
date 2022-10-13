import json
import asyncio
import time, datetime

import jellyfish
import pymongo
from work_project.mainpage import parsing_tools


def drop_collection_from_db(data_base, collection):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client[data_base]
    db.drop_collection(collection)


def get_collection_from_db(data_base, collection):
    client = pymongo.MongoClient('mongodb://localhost:27017')
    db = client[data_base]
    return db[collection]


def get_all_data_parser1():
    return parsing_tools.get_json_from_request('https://www.sec.gov/files/company_tickers.json')


def write_data_parser1(loc_json):
    companies = get_collection_from_db('db', 'companies')
    for company in loc_json:
        if companies.find_one({'cik_str': loc_json[company].get('cik_str')}) is None:
            companies.insert_one(loc_json[company])


def get_all_data_from_collection(collection):
    col = get_collection_from_db('db', collection)
    results = list(col.find())
    return results


def write_all_data_parser2(companies_data):
    companies_data_collection = get_collection_from_db('db', 'companies_data')
    ciks = [str(block.get('cik_str')).zfill(10) for block in companies_data]
    urls = [f'https://data.sec.gov/submissions/CIK{cik}.json' for cik in ciks]
    results = asyncio.run(parsing_tools.get_all_data_urls(urls, 2))
    for index, result in enumerate(results):
        companies_data_collection.insert_one(result)


def write_all_data_parser3(companies_data):
    npi_data = get_collection_from_db('db', 'npi_data')
    companies_collection = get_collection_from_db('db', 'companies')
    ciks = [c_json.get('cik_str') for c_json in companies_data]
    ciks = list(set(ciks))
    links1 = [
        f'https://api.orb-intelligence.com/3/search/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a&limit=10&cik={cik}'
        for cik in ciks]
    fisrt_data1 = asyncio.run(parsing_tools.get_all_data_urls(links1, 2))
    second_links = []
    unsearched_ciks = []
    for data1 in fisrt_data1:
        if data1.get('results_count') == 1:
            second_links.append(data1.get('results')[0].get('fetch_url'))
        else:
            unsearched_ciks.append(data1.get('request_fields').get('cik'))
    link_name_list = []

    for unsearched_cik in unsearched_ciks:
        searched_company = companies_collection.find_one({'cik_str': int(unsearched_cik)})
        link_name_list.append([
            f'https://api.orb-intelligence.com/3/search/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a&limit=10&ticker={(searched_company.get("ticker")).replace("-", "")}',
            searched_company.get("title")])

    links2 = [block[0] for block in link_name_list]
    fisrt_data2 = asyncio.run(parsing_tools.get_all_data_urls(links2, 2))
    for index, data in enumerate(fisrt_data2):
        for results_data in data.get('results'):
            if jellyfish.jaro_winkler_similarity(results_data.get('name').lower(),
                                                 link_name_list[index][1].lower()) > 0.85:
                second_links.append(results_data.get('fetch_url'))
                break
    second_data = asyncio.run(parsing_tools.get_all_data_urls(second_links, 2))
    cik_npi_list = [[data.get('cik'), data.get('npis')] for data in second_data if data.get('npis') != []]
    for cik, npi in cik_npi_list:
        if cik is not None and npi_data.find_one({'cik': str(cik)}) is None:
            npi_data.insert_one({'cik': cik, 'npi': npi})


def update_data():
    companies_col = get_collection_from_db('db', 'companies')
    new_data_json = get_all_data_parser1()
    if list(companies_col.find()) == []:
        write_data_parser1(get_all_data_parser1())
        companies_col_data = get_all_data_from_collection('companies')
        write_all_data_parser2(companies_col_data)
        write_all_data_parser3(companies_col_data)
    else:
        new_data = [new_data_json[data] for data in new_data_json]
        new_companies_list = [company for company in new_data if
                              companies_col.find_one({'cik_str': company.get('cik_str')}) is None]
        last_data = get_all_data_from_collection('companies')
        # print(new_companies_list)
        for cp in new_companies_list:
            companies_col.insert_one(cp)
        write_all_data_parser2(new_companies_list)
        # print(len(last_data), len(new_data), len(new_companies_list))
        write_all_data_parser3(new_companies_list)
    update_collection = get_collection_from_db('db', 'update_collection')
    drop_collection_from_db('db', 'update_collection')
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    update_collection.insert_one({'last_update': dt_string})


# write_all_data_parser2(get_all_data_from_collection('companies'))
if __name__ == '__main__':
    update_data()
    # print(get_collection_from_db('db', 'update_collection').find_one().get('last_update'))
