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
    count_new_npis = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_npis'}).get(
        'count_new_npis')
    count_records = npi_data_collection.count_documents({})
    return render(request, 'mainpage/npi_data.html',
                  {'npi_data': npi_data, 'updated_time': updated_time, 'count_new_npis': count_new_npis,
                   'count_records': count_records})


def nppes_data_page(request):
    return render(request, 'mainpage/../hhs/templates/nppes_list_data.html')


def nppes_data(request, npi_id):
    col = parsers.get_collection_from_db('db', 'nppes_data')
    nppes_npi_data = col.find_one({'NPI': str(npi_id)})
    if nppes_npi_data:
        return render(request, 'mainpage/../hhs/templates/nppes_data.html', context={'dataset': nppes_npi_data})


def display_nppes_data_individual(request):
    paginator = mongo_paginator(request, count_nppes_data_individual)
    part_npi = nppes_data_individual_collection.find().skip(500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'mainpage/../hhs/templates/nppes_individual.html', context={'dataset': part_npi, 'paginator': paginator})


def display_nppes_data_entities(request):
    paginator = mongo_paginator(request, count_nppes_data_entities)
    part_npi = nppes_data_entities_collection.find().skip(500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'mainpage/../hhs/templates/nppes_entities.html', context={'dataset': part_npi, 'paginator': paginator})


def mongo_paginator(request, count_docs):
    page = request.GET.get('page', 1)
    num_pages = count_docs // 500 + 1
    page_range = range(1, num_pages + 1)
    has_previous = True if int(page) > 1 else False
    number = int(page)
    previous_page_number = number - 1
    has_next = True if number < num_pages else False
    next_page_number = number + 1
    paginator = {'num_pages': num_pages, 'page_range': page_range, 'has_previous': has_previous, 'number': number,
                 'has_next': has_next, 'previous_page_number': previous_page_number,
                 'next_page_number': next_page_number}
    return paginator


def my_search(request):
    # print(request.GET)
    # print(request.GET['cik'])
    return render(request, 'mainpage/search_page.html')


def npi_data_search(request):
    cik = request.GET['cik']
    npi_data_collection = parsers.get_collection_from_db('db', 'npi_data')
    companies = list(npi_data_collection.find({'cik': {'$regex': str(cik)}}))
    return render(request, 'mainpage/npi_data_search.html',
                  {'npi_data': companies})


def nppes_data_search(request):
    print(request.GET)
    NPI = request.GET['NPI']
    companies = list(npees_data_collection.find({'NPI': {'$regex': NPI}}))
    return render(request, 'mainpage/../hhs/templates/nppes_data_search.html', {'dataset': companies})



