from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests, json
from GrowthPlug.settings import FB_BASE_API
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

fields=["category","name","phone","impressum","general_info","about","attire","bio","location","parking","hours","emails","website","description","company_overview","personal_info"]
fieldstring=','.join(fields)

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')

@require_http_methods(['GET'])
def home(request):
    return render(request, 'home.html')

@require_http_methods(['POST'])
@csrf_exempt
def getPages(request):
    user_access_token = request.POST.get('token', '')
    response = requests.get(("%s/me/accounts")%(FB_BASE_API), params = { "access_token" : user_access_token })
    response = response.json()
    user_pages = []
    for data in response['data']:
        temp = {}
        temp['access_token'] = data['access_token']
        temp['name'] = data['name']
        temp['id'] = data['id']
        temp['category'] = data['category']
        user_pages.append(temp)
    return render(request, 'dashboard.html', { "user_pages" : user_pages })


@csrf_exempt
def editPage(request):
    page_token = request.GET.get("pageToken", "")
    page_id = request.GET.get("pageId", "")
    response = requests.get(("%s/%s")%(FB_BASE_API, page_id), params = { "fields" : fieldstring, "access_token" : page_token })
    page_details = response.json()
    print(page_details)
    return render(request, 'pagedetails.html', { "page_details" : page_details, "page_token" : page_token })

@csrf_exempt
def updatePage(request):
    page_token = request.POST.get("pageToken", "")
    page_id = request.POST.get("pageId", "")
    pageData = {}
    pageData['access_token'] = page_token
    pageData['description'] = request.POST.get('description', "")
    pageData['impressum'] = request.POST.get('impressum', "")
    pageData['about'] = request.POST.get('about', "")
    pageData['phone'] = request.POST.get('phone', "")
    pageData['website'] = request.POST.get("website", "")
    pageData['company_overview'] = request.POST.get("company_overview", "")
    print(pageData)
    response = requests.post(("%s/%s")%(FB_BASE_API, page_id), data=pageData)
    print(response.json())
    return JsonResponse(response.json())