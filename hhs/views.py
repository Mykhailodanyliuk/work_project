from django.shortcuts import render
from mainpage import parsers
from mainpage.views import mongo_paginator


def hhs_page(request):
    return render(request, 'hhs/nppes_list_data.html')


def hhs_data_page(request, npi_id):
    nppes_data_entities_collection = parsers.get_collection_from_db('db', 'nppes_data_entities')
    nppes_data_individual_collection = parsers.get_collection_from_db('db', 'nppes_data_individual')
    col = parsers.get_collection_from_db('db', 'nppes_data')
    nppes_npi_data = col.find_one({'npi': str(npi_id)})
    if nppes_data_individual_collection.find_one({'npi': str(npi_id)}):
        nppes_npi_data = nppes_data_individual_collection.find_one({'npi': str(npi_id)})
    else:
        nppes_npi_data = nppes_data_entities_collection.find_one({'npi': str(npi_id)})
    if nppes_npi_data:
        return render(request, 'hhs/nppes_data.html', context={'dataset': nppes_npi_data.get('data')})


def display_hhs_data_individual(request):
    nppes_data_individual_collection = parsers.get_collection_from_db('db', 'nppes_data_individual')
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    counter_data = update_collection.find_one({'name': 'hhs_individuals'})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    paginator = mongo_paginator(request, collection_count_documents, 500)
    part_npi = nppes_data_individual_collection.find({},
                                                     {'_id': 0, 'npi': 1, 'data.provider_first_name': 1,
                                                      'data.provider_last_name__legal_name_': 1, 'upload_at': 1}).sort('npi').skip(
        500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'hhs/nppes_individual.html',
                  context={'dataset': part_npi, 'paginator': paginator, 'counter_data': counter_data})


def display_hhs_data_entities(request):
    nppes_data_entities_collection = parsers.get_collection_from_db('db', 'nppes_data_entities')
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    counter_data = update_collection.find_one({'name': 'hhs_entities'})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    paginator = mongo_paginator(request, collection_count_documents, 500)
    part_npi = nppes_data_entities_collection.find({}, {'_id': 0, 'npi': 1,
                                                        'data.provider_organization_name__legal_business_name_': 1,
                                                        'upload_at': 1}).sort('npi').skip(
        500 * (int(request.GET.get('page', 1)) - 1)).limit(500)
    return render(request, 'hhs/nppes_entities.html',
                  context={'dataset': part_npi, 'paginator': paginator, 'counter_data': counter_data})


def hhs_data_search(request):
    nppes_data_entities_collection = parsers.get_collection_from_db('db', 'nppes_data_entities')
    nppes_data_individual_collection = parsers.get_collection_from_db('db', 'nppes_data_individual')
    print(request.GET)
    NPI = request.GET['NPI']
    companies = list(
        nppes_data_entities_collection.find({'npi': {'$regex': NPI}}, {'_id': 0, 'npi': 1, 'upload_at': 1}))
    companies.extend(
        list(nppes_data_individual_collection.find({'npi': {'$regex': NPI}}, {'_id': 0, 'npi': 1, 'upload_at': 1})))
    print(companies)
    return render(request, 'hhs/nppes_data_search.html', {'dataset': companies})
