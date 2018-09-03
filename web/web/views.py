from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404

from .models import Projects, MainDomainResults, SubdomainResults, MailHarvestResults, DocResults, LinkedinCompanyInfo, LinkedinCompanyEmployees

def index_page(request):
    project_list = Projects.objects.all().order_by('project_id')
    return render_to_response('index.html',
                          {'project_data': project_list})

def view_projects(request, id):
    project_list = Projects.objects.filter(project_id=id)
    main_domain = MainDomainResults.objects.filter(project_id=id)
    subdomain = SubdomainResults.objects.filter(project_id=id)
    mail_harvest = MailHarvestResults.objects.filter(project_id=id)
    doc_result = DocResults.objects.filter(project_id=id)
    company_info = LinkedinCompanyInfo.objects.filter(project_id=id)
    company_employee = LinkedinCompanyEmployees.objects.filter(project_id=id)

    return render_to_response('projects.html', {'project_data' : project_list, 'main_domain' : main_domain, 'subdomain_results' : subdomain, 'mail_harvest' : mail_harvest, 'doc_result' : doc_result, 'company_info' : company_info, 'company_employee' : company_employee})

def about_page(request):
    return render_to_response('about.html')

def login_page(request):
    return render_to_response('login.html')
