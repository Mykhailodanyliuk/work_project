from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render
from . import parsers
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserLoginForm


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
    num_pages = count_docs // per_page + 1 if count_docs != per_page else 1
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


def get_sorted_data(request, collection, default_ordering, amount_data, keys):
    data_collection = parsers.get_collection_from_db('db', collection)
    update_collection = parsers.get_collection_from_db('db', 'update_collection')
    counter_data = update_collection.find_one({'name': collection})
    collection_count_documents = counter_data.get('total_records') if counter_data else 1
    order_by = request.GET.get('order_by') if (request.GET.get('order_by') is not None) else default_ordering
    page = int(request.GET.get('page', 1))
    paginator = mongo_paginator(request, collection_count_documents, amount_data)
    find_keys = {key: 1 for key in keys}
    context_data = list(
        data_collection.find({}, find_keys).sort(
            order_by).skip(amount_data * (page - 1)).limit(amount_data))
    return {'context_data': context_data, 'paginator': paginator, 'order_by': order_by, 'counter_data': counter_data}


def registration(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ви успішно зареєстровані")
            return redirect('main_page')
        else:
            messages.error(request, 'Помилка реєстрації')
    else:
        form = UserRegisterForm()
    return render(request, 'mainpage/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You are logged in")
            return redirect('main_page')
        else:
            messages.error(request, 'You entered an incorrect username or password')
            print(messages)
    else:
        form = UserLoginForm

    return render(request, 'mainpage/login.html', {"form": form})


def user_logout(request):
    logout(request)
    return redirect('main_page')
