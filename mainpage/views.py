from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from . import parsers
from json2html import *
from django.http import JsonResponse

def error_404(request, exception):
    return render(request, 'mainpage/404.html')


def error_500(request):
    return render(request, 'mainpage/404.html')


def index(request):
    return render(request, 'mainpage/mainpage.html')


def sec_company_fillings(request):
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
    npees_data_collection = parsers.get_collection_from_db('db', 'nppes_data')
    npis = npees_data_collection.distinct(key='NPI')
    page = request.GET.get('page', 1)
    paginator = Paginator(npis, 500)
    try:
        nppes = paginator.page(page)
    except PageNotAnInteger:
        nppes = paginator.page(1)
    except EmptyPage:
        nppes = paginator.page(paginator.num_pages)
    return render(request, 'mainpage/nppes_list_data.html', {'nppes_data': nppes})


def nppes_data(request, npi):
    col = parsers.get_collection_from_db('db', 'nppes_data')
    nppes_npi_data = col.find_one({'NPI': str(npi)})
    if nppes_npi_data:
        return render(request, 'mainpage/nppes_data.html', context={'dataset': nppes_npi_data})


def medical_trials(request):
    medical_trials_collection = parsers.get_collection_from_db('db', 'clinical_trials')
    organizations = medical_trials_collection.distinct(
        key='FullStudy.Study.ProtocolSection.IdentificationModule.Organization.OrgFullName')
    organizations_and_id = [[organization.replace(' ', '_'), organization]
                            for organization in organizations]
    page = request.GET.get('page', 1)
    paginator = Paginator(organizations_and_id, 500)
    try:
        part_organizations = paginator.page(page)
    except PageNotAnInteger:
        part_organizations = paginator.page(1)
    except EmptyPage:
        part_organizations = paginator.page(paginator.num_pages)
    return render(request, 'mainpage/medical_trials.html', context={'dataset': part_organizations})


def display_organization_trials(request, org_id):
    col = parsers.get_collection_from_db('db', 'clinical_trials')

    my_list = list(col.find(
        {'FullStudy.Study.ProtocolSection.IdentificationModule.Organization.OrgFullName': org_id.replace('_', ' ')}))
    print(len(my_list))
    # org_clinical_trials_list = list(org_clinical_trials)
    # print(org_clinical_trials_list)
    return render(request, 'mainpage/organization_clinical_trials.html', context={'dataset': my_list})

def display_clinical_trial(request, trial_id):
    print(trial_id)
    col = parsers.get_collection_from_db('db', 'clinical_trials')
    data = col.find_one({'FullStudy.Study.ProtocolSection.IdentificationModule.NCTId': trial_id})
    print(data)
    return render(request, 'mainpage/clinical_trial.html', context={'dataset': data})
