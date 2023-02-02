from django.shortcuts import render
from fda.views import paginate_data
from .models import Patent


def uspto_page(request):
    order_by = request.GET.get('order_by') if (request.GET.get('order_by') is not None) else 'patent_application_number'
    patents = Patent.objects.all().order_by(order_by)
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, patents, 50)
    return render(request, 'uspto/patents_page.html', {'context_data': context_data, 'paginator': context_data, 'order_by': order_by})


def uspto_patent_data(request, pk):
    patent_data = Patent.objects.get(pk=pk).data
    return render(request, 'uspto/patent_data.html', {'context_data': patent_data})
