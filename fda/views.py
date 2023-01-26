from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from .models import DeviceEvent, Device, DeviceEnforcement, DeviceRecall, DeviceClassification, DeviceCovid19, \
    DevicePMA, DeviceRegistrationListings, DeviceUDI, DrugEnforcement, DrugEvent, DrugNDC, FoodEnforcement, FoodEvent


def paginate_data(page, data, data_per_page):
    paginator = Paginator(data, data_per_page)
    try:
        context_data = paginator.page(page)
    except PageNotAnInteger:
        context_data = paginator.page(1)
    except EmptyPage:
        context_data = paginator.page(paginator.num_pages)
    return context_data


def fda_device_event_page(request):
    device_events = DeviceEvent.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_events, 50)
    return render(request, 'fda/fda_device_event.html', {'context_data': context_data, 'paginator': context_data})


def fda_device_event_data(request, pk):
    device_event_data = DeviceEvent.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_event_data.html', {'context_data': device_event_data})


def fda_device_page(request):
    device = Device.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device, 50)
    return render(request, 'fda/fda_device.html', {'context_data': context_data, 'paginator': context_data})


def fda_device_data(request, pk):
    device_data = Device.objects.get(pk=pk).data_json
    return render(request, 'fda/fda_device_data.html', {'context_data': device_data})


def fda_device_enforcement_page(request):
    device_enforcement = DeviceEnforcement.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_enforcement, 50)
    return render(request, 'fda/fda_device_enforcement_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_enforcement_data(request, pk):
    context_data = DeviceEnforcement.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_enforcement_data.html', {'context_data': context_data})


def fda_device_recall_page(request):
    device_recall = DeviceRecall.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_recall, 50)
    return render(request, 'fda/fda_device_recall_page.html', {'context_data': context_data, 'paginator': context_data})


def fda_device_recall_data(request, pk):
    context_data = DeviceRecall.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_recall_data.html', {'context_data': context_data})


def fda_device_classification_page(request):
    device_classification = DeviceClassification.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_classification, 50)
    return render(request, 'fda/fda_device_classification_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_classification_data(request, pk):
    context_data = DeviceClassification.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_classification_data.html', {'context_data': context_data})


def fda_device_covid19_page(request):
    device_covid19 = DeviceCovid19.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_covid19, 50)
    return render(request, 'fda/fda_device_covid19_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_covid19_data(request, pk):
    context_data = DeviceCovid19.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_covid19_data.html', {'context_data': context_data})


def fda_device_pma_page(request):
    device_pma = DevicePMA.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_pma, 50)
    return render(request, 'fda/fda_device_pma_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_pma_data(request, pk):
    context_data = DevicePMA.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_pma_data.html', {'context_data': context_data})


def fda_device_registration_listings_page(request):
    device_registration_listings = DeviceRegistrationListings.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_registration_listings, 50)
    return render(request, 'fda/fda_device_registration_listings_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_registration_listings_data(request, pk):
    context_data = DeviceRegistrationListings.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_registration_listings_data.html', {'context_data': context_data})


def fda_device_udi_page(request):
    device_udi = DeviceUDI.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, device_udi, 50)
    return render(request, 'fda/fda_device_udi_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_device_udi_data(request, pk):
    context_data = DeviceUDI.objects.get(pk=pk).data
    return render(request, 'fda/fda_device_udi_data.html', {'context_data': context_data})


def fda_drug_enforcement_page(request):
    drug_enforcement = DrugEnforcement.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, drug_enforcement, 50)
    return render(request, 'fda/fda_drug_enforcement_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_drug_enforcement_data(request, pk):
    context_data = DrugEnforcement.objects.get(pk=pk).data
    return render(request, 'fda/fda_drug_enforcement_data.html', {'context_data': context_data})


def fda_drug_event_page(request):
    drug_event = DrugEvent.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, drug_event, 50)
    return render(request, 'fda/fda_drug_event_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_drug_event_data(request, pk):
    context_data = DrugEvent.objects.get(pk=pk).data
    return render(request, 'fda/fda_drug_event_data.html', {'context_data': context_data})


def fda_drug_ndc_page(request):
    drug_ndc = DrugNDC.objects.all().order_by('labeler_name')
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, drug_ndc, 50)
    return render(request, 'fda/fda_drug_ndc_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_drug_ndc_data(request, pk):
    context_data = DrugNDC.objects.get(pk=pk).data
    return render(request, 'fda/fda_drug_ndc_data.html', {'context_data': context_data})


def fda_food_enforcement_page(request):
    food_enforcement = FoodEnforcement.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, food_enforcement, 50)
    return render(request, 'fda/fda_food_enforcement_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_food_enforcement_data(request, pk):
    context_data = FoodEnforcement.objects.get(pk=pk).data
    return render(request, 'fda/fda_food_enforcement_data.html', {'context_data': context_data})


def fda_food_event_page(request):
    food_event = FoodEvent.objects.all()
    page = request.GET.get('page', 1)
    context_data = paginate_data(page, food_event, 50)
    return render(request, 'fda/fda_food_event_page.html',
                  {'context_data': context_data, 'paginator': context_data})


def fda_food_event_data(request, pk):
    context_data = FoodEvent.objects.get(pk=pk).data
    return render(request, 'fda/fda_food_event_data.html', {'context_data': context_data})
