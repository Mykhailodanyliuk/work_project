from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from mainpage import parsers
from mainpage.views import get_sorted_data
from bson.objectid import ObjectId


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
    page_data = get_sorted_data(request, 'fda_device_event', 'report_number', 500, ['report_number', 'mdr_report_key',
                                                                                    'pma_pmn_number', 'upload_at'])
    return render(request, 'fda/fda_device_event.html',
                  page_data)


def fda_device_event_data(request, pk):
    device_event_collection = parsers.get_collection_from_db('db', 'fda_device_event')
    device_event_data = device_event_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_event_data.html', {'context_data': device_event_data})


def fda_device_page(request):
    page_data = get_sorted_data(request, 'fda_device_510k', 'device_name', 500,
                                ['device_name', 'k_number', 'applicant', 'upload_at'])
    return render(request, 'fda/fda_device.html',page_data)


def fda_device_data(request, pk):
    device_510k_collection = parsers.get_collection_from_db('db', 'fda_device_510k')
    device_510k_data = device_510k_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_data.html', {'context_data': device_510k_data})


def fda_device_enforcement_page(request):
    page_data = get_sorted_data(request, 'fda_device_enforcement', 'recall_number', 500,
                                ['recall_number', 'event_id', 'recalling_firm', 'upload_at'])
    return render(request, 'fda/fda_device_enforcement_page.html',page_data)


def fda_device_enforcement_data(request, pk):
    device_enforcement_collection = parsers.get_collection_from_db('db', 'fda_device_enforcement')
    context_data = device_enforcement_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_enforcement_data.html', {'context_data': context_data})


def fda_device_recall_page(request):
    page_data = get_sorted_data(request, 'fda_device_recall', 'cfres_id', 500,
                                ['cfres_id', 'res_event_number', 'recalling_firm', 'upload_at'])
    return render(request, 'fda/fda_device_recall_page.html',page_data)


def fda_device_recall_data(request, pk):
    device_recall_collection = parsers.get_collection_from_db('db', 'fda_device_recall')
    context_data = device_recall_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_recall_data.html', {'context_data': context_data})


def fda_device_classification_page(request):
    page_data = get_sorted_data(request, 'fda_device_classification', 'device_name', 500,
                                ['device_name', 'medical_specialty_description', 'regulation_number', 'upload_at'])
    return render(request, 'fda/fda_device_classification_page.html',page_data)


def fda_device_classification_data(request, pk):
    device_classification_collection = parsers.get_collection_from_db('db', 'fda_device_classification')
    context_data = device_classification_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_classification_data.html', {'context_data': context_data})


def fda_device_covid19_page(request):
    page_data = get_sorted_data(request, 'fda_device_covid19serology', 'sample_id', 500,
                                ['sample_id', 'lot_number', 'device', 'manufacturer', 'upload_at'])
    return render(request, 'fda/fda_device_covid19_page.html',page_data)


def fda_device_covid19_data(request, pk):
    device_covid19_collection = parsers.get_collection_from_db('db', 'fda_device_covid19serology')
    context_data = device_covid19_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_covid19_data.html', {'context_data': context_data})


def fda_device_pma_page(request):
    page_data = get_sorted_data(request, 'fda_device_pma', 'pma_number', 500,
                                ['pma_number', 'supplement_number', 'applicant', 'trade_name', 'upload_at'])
    return render(request, 'fda/fda_device_pma_page.html',page_data)


def fda_device_pma_data(request, pk):
    device_pma_collection = parsers.get_collection_from_db('db', 'fda_device_pma')
    context_data = device_pma_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_pma_data.html', {'context_data': context_data})


def fda_device_registration_listings_page(request):
    page_data = get_sorted_data(request, 'fda_device_registrationlisting', 'registration.registration_number', 500,
                                ['registration.registration_number', 'registration.fei_number', 'registration.name', 'upload_at'])
    return render(request, 'fda/fda_device_registration_listings_page.html',page_data)


def fda_device_registration_listings_data(request, pk):
    device_registration_listings_collection = parsers.get_collection_from_db('db', 'fda_device_registrationlisting')
    context_data = device_registration_listings_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_registration_listings_data.html', {'context_data': context_data})


def fda_device_udi_page(request):
    page_data = get_sorted_data(request, 'fda_device_udi', 'public_device_record_key', 500,
                                ['public_device_record_key', 'device_description', 'brand_name', 'upload_at'])
    return render(request, 'fda/fda_device_udi_page.html',page_data)


def fda_device_udi_data(request, pk):
    device_udi_collection = parsers.get_collection_from_db('db', 'fda_device_udi')
    context_data = device_udi_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_device_udi_data.html', {'context_data': context_data})


def fda_drug_enforcement_page(request):
    page_data = get_sorted_data(request, 'fda_drug_enforcement', 'recall_number', 500,
                                ['recall_number', 'event_id', 'recalling_firm', 'upload_at'])
    return render(request, 'fda/fda_drug_enforcement_page.html',page_data)


def fda_drug_enforcement_data(request, pk):
    drug_enforcement_collection = parsers.get_collection_from_db('db', 'fda_drug_enforcement')
    context_data = drug_enforcement_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_drug_enforcement_data.html', {'context_data': context_data})


def fda_drug_event_page(request):
    page_data = get_sorted_data(request, 'fda_drug_event', 'safetyreportid', 500,
                                ['safetyreportid', 'companynumb', 'upload_at'])
    return render(request, 'fda/fda_drug_event_page.html',page_data)


def fda_drug_event_data(request, pk):
    drug_event_collection = parsers.get_collection_from_db('db', 'fda_drug_event')
    context_data = drug_event_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_drug_event_data.html', {'context_data': context_data})


def fda_drug_ndc_page(request):
    page_data = get_sorted_data(request, 'fda_drug_ndc', 'product_ndc', 500,
                                ['product_ndc', 'labeler_name', 'upload_at'])
    return render(request, 'fda/fda_drug_ndc_page.html',page_data)


def fda_drug_ndc_data(request, pk):
    drug_ndc_collection = parsers.get_collection_from_db('db', 'fda_drug_ndc')
    context_data = drug_ndc_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_drug_ndc_data.html', {'context_data': context_data})


def fda_food_enforcement_page(request):
    page_data = get_sorted_data(request, 'fda_food_enforcement', 'recall_number', 500,
                                ['recall_number', 'event_id', 'recalling_firm', 'upload_at'])
    return render(request, 'fda/fda_food_enforcement_page.html',page_data)


def fda_food_enforcement_data(request, pk):
    food_enforcement_collection = parsers.get_collection_from_db('db', 'fda_food_enforcement')
    context_data = food_enforcement_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_food_enforcement_data.html', {'context_data': context_data})


def fda_food_event_page(request):
    page_data = get_sorted_data(request, 'fda_food_event', 'report_number', 500,
                                ['report_number', 'upload_at'])
    return render(request, 'fda/fda_food_event_page.html',page_data)


def fda_food_event_data(request, pk):
    food_event_collection = parsers.get_collection_from_db('db', 'fda_food_event')
    context_data = food_event_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_food_event_data.html', {'context_data': context_data})


def fda_drug_label_page(request):
    page_data = get_sorted_data(request, 'fda_drug_label', 'set_id', 500,
                                ['set_id', 'id', 'upload_at'])
    return render(request, 'fda/fda_drug_label_page.html',page_data)


def fda_drug_label_data(request, pk):
    food_event_collection = parsers.get_collection_from_db('db', 'fda_drug_label')
    context_data = food_event_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_drug_label_data.html', {'context_data': context_data})


def fda_other_nsde_page(request):
    page_data = get_sorted_data(request, 'fda_other_nsde', 'proprietary_name', 500,
                                ['proprietary_name', 'application_number_or_citation', 'package_ndc', 'upload_at'])
    return render(request, 'fda/fda_other_nsde_page.html',page_data)


def fda_other_nsde_data(request, pk):
    fda_other_nsde_collection = parsers.get_collection_from_db('db', 'fda_other_nsde')
    context_data = fda_other_nsde_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_other_nsde_data.html', {'context_data': context_data})


def fda_other_substance_page(request):
    page_data = get_sorted_data(request, 'fda_other_substance', 'uuid', 500,
                                ['uuid', 'unii', 'substance_class', 'upload_at'])
    return render(request, 'fda/fda_other_substance_page.html',page_data)


def fda_other_substance_data(request, pk):
    fda_other_substance_collection = parsers.get_collection_from_db('db', 'fda_other_substance')
    context_data = fda_other_substance_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_other_substance_data.html', {'context_data': context_data})


def fda_tobacco_problem_page(request):
    page_data = get_sorted_data(request, 'fda_tobacco_problem', 'report_id', 500,
                                ['report_id', 'upload_at'])
    return render(request, 'fda/fda_tobacco_problem_page.html',page_data)


def fda_tobacco_problem_data(request, pk):
    fda_tobacco_problem_collection = parsers.get_collection_from_db('db', 'fda_tobacco_problem')
    context_data = fda_tobacco_problem_collection.find_one(ObjectId(pk))
    return render(request, 'fda/fda_tobacco_problem_data.html', {'context_data': context_data})


def fda_animalandveterinary_event_page(request):
    page_data = get_sorted_data(request, 'fda_animalandveterinary_event', 'unique_aer_id_number', 500,
                                ['unique_aer_id_number', 'report_id', 'type_of_information', 'upload_at'])
    return render(request, 'fda/fda_animalandveterinary_event_page.html',page_data)


def fda_animalandveterinary_event_data(request, pk):
    fda_animalandveterinary_event_collection = parsers.get_collection_from_db('db', 'fda_animalandveterinary_event')
    context_data = fda_animalandveterinary_event_collection.find_one(ObjectId(pk))
    print(context_data)
    return render(request, 'fda/fda_animalandveterinary_event_data.html', {'context_data': context_data})
