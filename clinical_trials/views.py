from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from mainpage import parsers

clinical_trial_organizations_collection = parsers.get_collection_from_db('db', 'clinical_trials_organizations')
clinical_trials_collection = parsers.get_collection_from_db('db', 'clinical_trials')


def display_clinical_trials_organizations(request):
    organizations_and_id = [[organization.get('organization').replace(' ', '_'), organization.get('organization')]
                            for organization in
                            clinical_trial_organizations_collection.find({}, {'_id': 0, 'organization': 1})]
    count_organizations = len(organizations_and_id)
    page = request.GET.get('page', 1)
    paginator = Paginator(organizations_and_id, 500)
    try:
        part_organizations = paginator.page(page)
    except PageNotAnInteger:
        part_organizations = paginator.page(1)
    except EmptyPage:
        part_organizations = paginator.page(paginator.num_pages)
    return render(request, 'clinical_trials/clinical_trials_organizations.html',
                  context={'dataset': part_organizations, 'count': count_organizations,
                           'paginator': part_organizations})


def display_organization_trials(request, org_id):
    my_list = list(clinical_trial_organizations_collection.find({'organization': org_id.replace('_', ' ')}))
    return render(request, 'clinical_trials/organization_clinical_trials.html', context={'dataset': my_list[0]})


def display_clinical_trial(request, trial_id):
    data = clinical_trials_collection.find_one({'nct_id': trial_id})
    return render(request, 'clinical_trials/clinical_trial.html', context={'dataset': data})


def clinical_trials_organization_search(request):
    npi = request.GET['organization']
    dataset = [[organization.get('organization').replace(' ', '_'), organization.get('organization')]
               for organization in
               clinical_trial_organizations_collection.find({'organization': {'$regex': npi}},
                                                            {'_id': 0, 'organization': 1})]
    return render(request, 'clinical_trials/clinical_trials_organization_search.html',
                  {'dataset': dataset, 'paginator': dataset})
