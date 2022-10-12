from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from . import parsers
from json2html import *

def error_404(request, exception):
    return render(request, 'mainpage/404.html')


def error_500(request):
    return render(request, 'mainpage/404.html')


def index(request):
    return render(request, 'mainpage/mainpage.html')


def update_data(request):
    parsers.delete_and_download_data()
    return render(request, 'mainpage/data_update.html')

def download_data(request):
    if request.method == 'POST':
        parsers.delete_and_download_data()
        return redirect('/')
    return render(request, 'mainpage/data_download.html')


def data_management(request):
    return render(request, 'mainpage/data_management.html')


def get_company_data(request, cik):
    col = parsers.get_collection_from_db('db', 'companies_data')
    company_data = col.find_one({'cik': cik})
    c_data = {}
    if not company_data:
        company_data = col.find_one({'cik': cik.zfill(10)})
    # company_data['']
    if company_data:
        for key, value in company_data.items():
            if type(value) == list:
                try:
                    company_data[key] = ','.join(value)
                except TypeError:
                    pass
        return render(request, 'mainpage/company_data.html', context={'dataset': company_data})


def get_list_companies_page(request):
    companies_data = parsers.get_all_data_from_collection('companies')
    page = request.GET.get('page', 1)
    paginator = Paginator(companies_data, 500)
    try:
        companies = paginator.page(page)
    except PageNotAnInteger:
        companies = paginator.page(1)
    except EmptyPage:
        companies = paginator.page(paginator.num_pages)
    return render(request, 'mainpage/companies_data.html', {'companies': companies})


def get_list_npi_data(request):
    npi_data = parsers.get_all_data_from_collection('npi_data')
    return render(request, 'mainpage/npi_data.html', {'npi_data': npi_data})
