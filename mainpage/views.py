import json

import pymongo
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from . import parsers
from json2html import *
from django.http import JsonResponse

mycollection = parsers.get_collection_from_db('db', 'nppes_data')
npees_data_collection = parsers.get_collection_from_db('db', 'nppes_data')
# clinical_trial_individual_collection_data = parsers.get_all_data_from_collection('nppes_data_individual')
# clinical_trial_entities_collection_data = parsers.get_all_data_from_collection('nppes_data_entities')
clinical_trial_individual_collection_data = list(mycollection.find({'Entity Type Code': '1'},
                                  {'NPI': 1, '_id': 0, 'Provider First Name': 1, 'Provider Last Name (Legal Name)': 1}))
clinical_trial_entities_collection_data = list(mycollection.find({'Entity Type Code': '2'}, {'NPI': 1, '_id': 0, 'Provider Organization Name (Legal Business Name)':1}))


def error_404(request, exception):
    return render(request, 'mainpage/404.html')


def error_500(request):
    return render(request, 'mainpage/404.html')


def index(request):
    return render(request, 'mainpage/mainpage.html')


def sec_company_fillings(request):
    companies_cik_ein_col = parsers.get_collection_from_db('db', 'companies_cik_ein')
    companies_cik_ein_data = parsers.get_all_data_from_collection('companies_cik_ein')
    # companies_data = parsers.get_all_data_from_collection('companies')
    # companies_collection = parsers.get_collection_from_db('db', 'companies')
    page = request.GET.get('page', 1)
    paginator = Paginator(companies_cik_ein_data, 500)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    updated_time = parsers.get_collection_from_db('db', 'update_collection').find_one({'name': 'last_update'}).get(
        'update_time')
    count_new_companies = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_companies'}).get(
        'count_new_companies')
    count_records = companies_cik_ein_col.count_documents({})
    return render(request, 'mainpage/sec_company_fillings.html',
                  {'companies': companies, 'updated_time': updated_time, 'count_new_companies': count_new_companies,
                   'count_records': count_records})


def get_company_data(request, cik):
    col = parsers.get_collection_from_db('db', 'companies_data')
    company_data = col.find_one({'cik': cik})
    if not company_data:
        company_data = col.find_one({'cik': cik.zfill(10)})
    if company_data:
        filings_recent = company_data.get('filings').get('recent').items()
        return render(request, 'mainpage/company_data.html',
                      context={'dataset': company_data, 'filings_recent': filings_recent})


def sec_company_tickers(request):
    companies_data = parsers.get_all_data_from_collection('companies')
    companies_collection = parsers.get_collection_from_db('db', 'companies')
    page = request.GET.get('page', 1)
    paginator = Paginator(companies_data, 500)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    updated_time = parsers.get_collection_from_db('db', 'update_collection').find_one({'name': 'last_update'}).get(
        'update_time')
    count_new_companies = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_companies'}).get(
        'count_new_companies')
    count_records = companies_collection.count_documents({})
    return render(request, 'mainpage/sec_company_tickers.html',
                  {'companies': companies, 'updated_time': updated_time, 'count_new_companies': count_new_companies,
                   'count_records': count_records})


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
    return render(request, 'mainpage/nppes_list_data.html')


def nppes_data(request, npi_id):
    col = parsers.get_collection_from_db('db', 'nppes_data')
    nppes_npi_data = col.find_one({'NPI': str(npi_id)})
    if nppes_npi_data:
        return render(request, 'mainpage/nppes_data.html', context={'dataset': nppes_npi_data})


def medical_trials(request):
    medical_trial_organizations_collection = parsers.get_collection_from_db('db', 'clinical_trials_organizations')
    organizations = [record['organization'] for record in medical_trial_organizations_collection.find()]
    organizations_and_id = [[organization.replace(' ', '_'), organization]
                            for organization in list(organizations)]
    count_organizations = len(organizations_and_id)

    page = request.GET.get('page', 1)
    paginator = Paginator(organizations_and_id, 500)
    try:
        part_organizations = paginator.page(page)
    except PageNotAnInteger:
        part_organizations = paginator.page(1)
    except EmptyPage:
        part_organizations = paginator.page(paginator.num_pages)
    return render(request, 'mainpage/medical_trials.html',
                  context={'dataset': part_organizations, 'count': count_organizations})


def display_organization_trials(request, org_id):
    clinical_trial_organizations_collection = parsers.get_collection_from_db('db', 'clinical_trials_organizations')
    my_list = list(clinical_trial_organizations_collection.find({'organization': org_id.replace('_', ' ')}))
    print(my_list)
    return render(request, 'mainpage/organization_clinical_trials.html', context={'dataset': my_list[0]})


def display_clinical_trial(request, trial_id):
    print(trial_id)
    col = parsers.get_collection_from_db('db', 'clinical_trials')
    data = col.find_one({'nct_id': trial_id})
    print(data)
    return render(request, 'mainpage/clinical_trial.html', context={'dataset': data})


def display_clinical_trial_individual(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(clinical_trial_individual_collection_data, 500)
    try:
        part_npi = paginator.page(page)
    except PageNotAnInteger:
        part_npi = paginator.page(1)
    except EmptyPage:
        part_npi = paginator.page(paginator.num_pages)
    print(part_npi)
    return render(request, 'mainpage/nppes_individual.html', context={'dataset': part_npi})


def display_clinical_trial_entities(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(clinical_trial_entities_collection_data, 500)
    try:
        part_npi = paginator.page(page)
    except PageNotAnInteger:
        part_npi = paginator.page(1)
    except EmptyPage:
        part_npi = paginator.page(paginator.num_pages)
    print(part_npi)
    return render(request, 'mainpage/nppes_entities.html', context={'dataset': part_npi})
