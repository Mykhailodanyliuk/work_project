from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from mainpage import parsers
from mainpage.views import mongo_paginator


def sec_company_fillings(request):
    companies_data_collection = parsers.get_collection_from_db('db', 'sec_data')
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    counter_data = update_collection.find_one({'name': 'sec_data'})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    order_by = request.GET.get('order_by') if (request.GET.get('order_by') is not None) else 'name'
    page = int(request.GET.get('page', 1))
    paginator = mongo_paginator(request, collection_count_documents, 500)
    companies = companies_data_collection.find({}, {'_id': 0, 'name': 1, 'cik': 1, 'ein': 1, 'upload_date': 1}).sort(
        'name').skip(500 * (page - 1)).limit(500)
    if order_by == 'cik':
        companies = companies_data_collection.find({},
                                                   {'_id': 0, 'name': 1, 'cik': 1, 'ein': 1, 'upload_date': 1}).sort(
            'cik').skip(500 * (page - 1)).limit(500)
    return render(request, 'sec/sec_company_fillings.html',
                  {'paginator': paginator, 'companies': companies, 'counter_data': counter_data, 'order_by': order_by})


def display_sec_company_data(request, cik):
    sec_data_fillings_collection = parsers.get_collection_from_db('db', 'sec_data')
    company_data = sec_data_fillings_collection.find_one({'cik': cik}).get('data')
    filings_recent = company_data.get('filings').get('recent').items()
    links = [f'https://www.sec.gov/Archives/edgar/data/{cik.lstrip("0")}/{i.replace("-", "")}/{i}-index.html' for i in
             company_data.get('filings').get('recent').get('accessionNumber')]
    filings_values = list(company_data.get('filings').get('recent').values())
    filings_values.insert(0, links)
    fillings_all_data = []
    for m in range(len(links)):
        part_data = []
        for value in filings_values:
            part_data.append(value[m])
        fillings_all_data.append(part_data)
    return render(request, 'sec/sec_company_data.html',
                  context={'dataset': company_data, 'filings_recent': filings_recent, 'links': links,
                           'fillings_all_data': fillings_all_data})


def sec_company_tickers(request):
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    sec_data_tickers_collection = parsers.get_collection_from_db('db', 'sec_data_tickers')
    counter_data = update_collection.find_one({'name': 'sec_tickers'})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    order_by = request.GET.get('order_by') if (request.GET.get('order_by') is not None) else 'name'
    page = int(request.GET.get('page', 1))
    paginator = mongo_paginator(request, collection_count_documents, 500)
    companies = sec_data_tickers_collection.find({}, {'_id': 0, 'title': 1, 'cik_str': 1, 'tickers': 1, 'upload_at': 1}).sort(
        'name').skip(500 * (page - 1)).limit(500)
    if order_by == 'cik':
        companies = sec_data_tickers_collection.find({},
                                                     {'_id': 0, 'title': 1, 'cik_str': 1, 'tickers': 1, 'upload_at': 1}).sort(
            'cik').skip(500 * (page - 1)).limit(500)
    return render(request, 'sec/sec_company_tickers.html',
                  {'companies': companies, 'counter_data': counter_data, 'paginator': paginator})


def sec_company_tickers_search(request):
    cik = request.GET['cik']
    companies_collection = parsers.get_collection_from_db('db', 'companies')
    companies = list(companies_collection.find({'cik_str': int(cik)})) if cik.isnumeric() else []
    return render(request, 'sec/sec_company_tickers_search.html',
                  {'companies': companies})


def sec_company_fillings_search(request):
    companies_data_collection = parsers.get_collection_from_db('db', 'sec_data')
    cik = request.GET['cik']
    companies = list(companies_data_collection.find({'cik': {'$regex': cik}}))
    return render(request, 'sec/sec_company_fillings_search.html',
                  {'companies': companies})
