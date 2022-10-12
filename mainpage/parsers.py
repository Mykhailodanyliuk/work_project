import json
import asyncio
import jellyfish
import pymongo
from . import parsing_tools


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
        companies.insert_one(loc_json[company])


def get_all_data_from_collection(collection):
    col = get_collection_from_db('db', collection)
    results = list(col.find())
    return results


def write_all_data_parser2():
    companies_data = get_collection_from_db('db', 'companies_data1')
    companies_collection = get_all_data_from_collection('companies')
    ciks = [str(block.get('cik_str')).zfill(10) for block in companies_collection]
    ciks = list(set(ciks))
    urls = [f'https://data.sec.gov/submissions/CIK{cik}.json' for cik in ciks]
    results = asyncio.run(parsing_tools.get_all_data_urls(urls, 2))
    for index, result in enumerate(results):
        companies_data.insert_one(result)


def write_all_data_parser3():
    npi_data = get_collection_from_db('db', 'npi_data')
    companies_collection = get_all_data_from_collection('companies')
    ciks = [c_json.get('cik_str') for c_json in companies_collection]
    ciks = list(set(ciks))
    links1 = [
        f'https://api.orb-intelligence.com/3/search/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a&limit=10&cik={cik}'
        for cik in ciks]
    fisrt_data1 = asyncio.run(parsing_tools.get_all_data_urls(links1, 2))
    second_links = []
    unsearched_ciks = []
    for data1 in fisrt_data1:
        print(data1)
        if data1.get('results_count') == 1:
            second_links.append(data1.get('results')[0].get('fetch_url'))
        else:
            unsearched_ciks.append(data1.get('request_fields').get('cik'))
    print(unsearched_ciks)
    link_name_list = []
    for unsearched_cik in unsearched_ciks:
        for company_data in companies_collection:
            if str(company_data.get('cik_str')) == unsearched_cik:
                link_name_list.append([
                    f'https://api.orb-intelligence.com/3/search/?api_key=c66c5dad-395c-4ec6-afdf-7b78eb94166a&limit=10&ticker={(company_data.get("ticker")).replace("-", "")}',
                    company_data.get("title")])
                break
    links2 = [block[0] for block in link_name_list]
    fisrt_data2 = asyncio.run(parsing_tools.get_all_data_urls(links2, 2))
    for index, data in enumerate(fisrt_data2):
        for results_data in data.get('results'):
            print(results_data.get('name'), link_name_list[index][1])
            if jellyfish.jaro_winkler_similarity(results_data.get('name').lower(),
                                                 link_name_list[index][1].lower()) > 0.85:
                print('EII')
                second_links.append(results_data.get('fetch_url'))
                break
    second_data = asyncio.run(parsing_tools.get_all_data_urls(second_links, 2))
    cik_npi_list = [[data.get('cik'), data.get('npis')] for data in second_data if data.get('npis') != []]
    print(len(cik_npi_list))
    for cik, npi in cik_npi_list:
        if cik is not None:
            npi_data.insert_one({'cik': cik, 'npi': npi})

    # name_zip_cik_list = []
    # data = get_all_data_from_collection('companies_data')
    # for company in data:
    #     company_name = company.get('name')
    #     first_word_name = company_name.split()[0]
    #     try:
    #         postal_code = company.get('addresses').get('mailing').get('zipCode')[:5]
    #     except:
    #         continue
    #     cik = company.get('cik')
    #     name_zip_cik_list.append([first_word_name, postal_code, str(cik).zfill(10), company_name])
    #     # print(first_word_name,postal_code)
    # urls = [
    #     f'https://npiregistry.cms.hhs.gov/api/?number=&enumeration_type=&taxonomy_description=&first_name=&use_first_name_alias=&last_name=&organization_name={block[0]}*&address_purpose=&city=&state=&postal_code={block[1]}*&country_code=&limit=&skip=&pretty=&version=2.1'
    #     for block in name_zip_cik_list]
    # results = asyncio.run(get_all_data_urls(urls, 100))
    # for index, result in enumerate(results):
    #     print(name_zip_cik_list[index][3])
    #     if result.get('result_count') != 0 and result.get('Errors') is None:
    #         npi_data.insert_one({str(name_zip_cik_list[index][3]): result})


def delete_and_download_data():
    drop_collection_from_db('db', 'companies')
    # drop_collection_from_db('db', 'companies_data')
    # drop_collection_from_db('db', 'npi_data')
    write_data_parser1(get_all_data_parser1())
    # write_all_data_parser2()
    # write_all_data_parser3()
def update_data():
    print('Update data')

# if __name__ == '__main__':
#     pass
