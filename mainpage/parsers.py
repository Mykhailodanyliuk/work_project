import asyncio
import time, datetime
import jellyfish
import pymongo

from medical_site.settings import BASE_DIR, env
from . import parsing_tools
import pytz
from ssh_pymongo import MongoSession

# def drop_collection_from_db(data_base, collection):
#     client = pymongo.MongoClient('mongodb://host.docker.internal:27017')
#     db = client[data_base]
#     db.drop_collection(collection)

session = MongoSession(
    host=env('MONGO_HOST'),
    port=2222,
    user=env('MONGO_USER'),
    password=env('MONGO_PASSWORD'),
)


def get_collection_from_db(data_base, collection):
    # client = pymongo.MongoClient('mongodb://localhost:27017')
    # db = client[data_base]
    # return db[collection]

    db = session.connection[data_base]
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


if __name__ == '__main__':
    while True:
        time.sleep(43200)
