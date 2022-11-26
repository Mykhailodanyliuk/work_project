from django.shortcuts import render
from mainpage import parsers
from mainpage.views import mongo_paginator

mycollection = parsers.get_collection_from_db('db', 'nppes_data')
npees_data_collection = parsers.get_collection_from_db('db', 'nppes_data')
nppes_data_individual_collection = parsers.get_collection_from_db('db', 'nppes_data_individual')
nppes_data_entities_collection = parsers.get_collection_from_db('db', 'nppes_data_entities')
count_nppes_data_individual = nppes_data_individual_collection.count_documents({})
count_nppes_data_entities = nppes_data_entities_collection.count_documents({})


def hhs_page(request):
    return render(request, 'hhs/nppes_list_data.html')


def hhs_data_page(request, npi_id):
    col = parsers.get_collection_from_db('db', 'nppes_data')
    nppes_npi_data = col.find_one({'NPI': str(npi_id)})
    if nppes_npi_data:
        return render(request, 'hhs/nppes_data.html', context={'dataset': nppes_npi_data})


def display_hhs_data_individual(request):
    paginator = mongo_paginator(request, count_nppes_data_individual)
    part_npi = nppes_data_individual_collection.find().skip(500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'hhs/nppes_individual.html', context={'dataset': part_npi, 'paginator': paginator})


def display_hhs_data_entities(request):
    paginator = mongo_paginator(request, count_nppes_data_entities)
    part_npi = nppes_data_entities_collection.find().skip(500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'hhs/nppes_entities.html', context={'dataset': part_npi, 'paginator': paginator})


def hhs_data_search(request):
    print(request.GET)
    NPI = request.GET['NPI']
    companies = list(npees_data_collection.find({'NPI': {'$regex': NPI}}))
    return render(request, 'hhs/nppes_data_search.html', {'dataset': companies})
