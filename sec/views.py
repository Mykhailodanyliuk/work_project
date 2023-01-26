from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from mainpage import parsers

companies_data_collection = parsers.get_collection_from_db('db', 'companies_data')
count_companies_data = companies_data_collection.count_documents({})


def sec_company_fillings(request):
    order_by = request.GET.get('order_by')
    page = request.GET.get('page', 1)
    num_pages = count_companies_data // 500 + 1
    page_range = range(1, num_pages + 1)
    has_previous = True if int(page) > 1 else False
    number = int(page)
    previous_page_number = number - 1
    has_next = True if number < num_pages else False
    next_page_number = number + 1
    dataset1 = {
        'paginator': {'num_pages': num_pages, 'page_range': page_range, 'previous_page_number': previous_page_number},
        'has_previous': has_previous, 'number': number,
        'has_next': has_next,
        'next_page_number': next_page_number}

    companies = companies_data_collection.find({}, {'_id': 0, 'name': 1, 'cik': 1, 'ein': 1}).sort('name').skip(
        500 * (number - 1)).limit(500)

    if order_by == 'cik':
        companies = companies_data_collection.find({}, {'_id': 0, 'name': 1, 'cik': 1, 'ein': 1}).sort('cik').skip(
            500 * (number - 1)).limit(500)
    # companies = companies_data_collection.find().skip(500 * (number - 1)).limit(500)
    updated_time = parsers.get_collection_from_db('db', 'update_collection').find_one({'name': 'last_update'}).get(
        'update_time')
    count_new_records = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_companies'}).get(
        'count_new_companies')
    count_records = companies_data_collection.count_documents({})
    counter_data = {'updated_time': updated_time, 'count_new_records': count_new_records, 'renewal_period': '',
                    'count_records': count_records}
    return render(request, 'sec/sec_company_fillings.html',
                  {'paginator': dataset1, 'companies': companies, 'counter_data': counter_data, 'order_by': order_by})


def display_sec_company_data(request, cik):
    col = parsers.get_collection_from_db('db', 'companies_data')
    company_data = col.find_one({'cik': cik})
    if not company_data:
        company_data = col.find_one({'cik': cik.zfill(10)})
    # if company_data:
    filings_recent = company_data.get('filings').get('recent').items()
    cik = cik.lstrip('0')
    links = [f'https://www.sec.gov/Archives/edgar/data/{cik}/{i.replace("-", "")}/{i}-index.html' for i in
             company_data.get('filings').get('recent').get('accessionNumber')]
    filings_values = list(company_data.get('filings').get('recent').values())
    filings_len = len(company_data.get('filings').get('recent'))
    filings_recent_data = [
        [filings_values[k][m] for k in range(filings_len)]
        for m in range(len(company_data.get('filings').get('recent').get('accessionNumber')))
    ]
    fillings_all_data = []
    for m in range(len(company_data.get('filings').get('recent').get('accessionNumber'))):
        part_data = []
        part_data.append(
            f"https://www.sec.gov/Archives/edgar/data/{cik}/{company_data.get('filings').get('recent').get('accessionNumber')[m].replace('-', '')}/{m}-index.html")
        for k in range(filings_len):
            part_data.append(filings_values[k][m])
        fillings_all_data.append(part_data)
    return render(request, 'sec/sec_company_data.html',
                  context={'dataset': company_data, 'filings_recent': filings_recent, 'links': links,
                           'fillings_all_data': fillings_all_data})


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
    count_new_records = parsers.get_collection_from_db('db', 'update_collection').find_one(
        {'name': 'new_companies'}).get(
        'count_new_companies')
    count_records = companies_collection.count_documents({})
    counter_data = {'updated_time': updated_time, 'count_new_records': count_new_records, 'renewal_period': '',
                    'count_records': count_records}
    return render(request, 'sec/sec_company_tickers.html',
                  {'companies': companies, 'counter_data': counter_data, 'paginator': companies})


def sec_company_tickers_search(request):
    cik = request.GET['cik']
    companies_collection = parsers.get_collection_from_db('db', 'companies')
    companies = list(companies_collection.find({'cik_str': int(cik)})) if cik.isnumeric() else []
    return render(request, 'sec/sec_company_tickers_search.html',
                  {'companies': companies})


def sec_company_fillings_search(request):
    cik = request.GET['cik']
    companies = list(companies_data_collection.find({'cik': {'$regex': cik}}))
    return render(request, 'sec/sec_company_fillings_search.html',
                  {'companies': companies})
