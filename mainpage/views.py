from django.shortcuts import render
from . import parsers

mycollection = parsers.get_collection_from_db('db', 'nppes_data')
npees_data_collection = parsers.get_collection_from_db('db', 'nppes_data')
nppes_data_individual_collection = parsers.get_collection_from_db('db', 'nppes_data_individual')
nppes_data_entities_collection = parsers.get_collection_from_db('db', 'nppes_data_entities')
count_nppes_data_individual = nppes_data_individual_collection.count_documents({})
count_nppes_data_entities = nppes_data_entities_collection.count_documents({})


def error_404(request, exception):
    return render(request, 'mainpage/404.html')


def error_500(request):
    return render(request, 'mainpage/404.html')


def index(request):
    return render(request, 'mainpage/mainpage.html')


def get_list_npi_data(request):
    npi_data_collection = parsers.get_collection_from_db('db', 'npi_data')
    npi_data = parsers.get_all_data_from_collection('npi_data')
    updated_time = parsers.get_collection_from_db('db', 'update_collection').find_one({'name': 'last_update'}).get(
        'update_time')
    count_new_records = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_npis'}).get(
        'count_new_npis')
    count_records = npi_data_collection.count_documents({})
    counter_data = {'updated_time': updated_time, 'count_new_records': count_new_records, 'renewal_period': '',
                    'count_records': count_records}
    return render(request, 'mainpage/npi_data.html',
                  {'npi_data': npi_data, 'counter_data': counter_data})


def npi_data_search(request):
    cik = request.GET['cik']
    npi_data_collection = parsers.get_collection_from_db('db', 'npi_data')
    companies = list(npi_data_collection.find({'cik': {'$regex': str(cik)}}))
    return render(request, 'mainpage/npi_data_search.html',
                  {'npi_data': companies})


def mongo_paginator(request, count_docs, per_page):
    page = request.GET.get('page', 1)
    num_pages = count_docs // per_page + 1
    page_range = range(1, num_pages + 1)
    has_previous = True if int(page) > 1 else False
    number = int(page)
    previous_page_number = number - 1
    has_next = True if number < num_pages else False
    next_page_number = number + 1
    paginator = {
        'paginator': {'num_pages': num_pages, 'page_range': page_range, 'previous_page_number': previous_page_number},
        'has_previous': has_previous, 'number': number,
        'has_next': has_next,
        'next_page_number': next_page_number}
    return paginator
