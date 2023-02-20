from bson import ObjectId
from django.shortcuts import render
from mainpage import parsers
from mainpage.views import get_sorted_data


def uspto_page(request):
    page_data = get_sorted_data(request, 'uspto_data', 'patentApplicationNumber', 500,
                                ['patentApplicationNumber', 'inventionTitle', 'upload_at'])
    return render(request, 'uspto/patents_page.html',
                  {'context_data': page_data.get('context_data'), 'paginator': page_data.get('paginator'),
                   'order_by': page_data.get('order_by')})


def uspto_patent_data(request, pk):
    uspto_data_collection = parsers.get_collection_from_db('db', 'uspto_data')
    context_data = uspto_data_collection.find_one(ObjectId(pk))
    return render(request, 'uspto/patent_data.html', {'context_data': context_data})
