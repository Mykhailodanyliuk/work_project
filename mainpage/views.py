from django.shortcuts import render
from . import parsers


def error_404(request, exception):
    return render(request, 'mainpage/404.html')


def error_500(request):
    return render(request, 'mainpage/404.html')


def index(request):
    return render(request, 'mainpage/mainpage.html')


def get_list_npi_data(request):
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    npi_data_collection = parsers.get_collection_from_db('db', 'npi_data')
    counter_data = update_collection.find_one({'name': 'npi_data'})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    npi_data = npi_data_collection.find({})
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
