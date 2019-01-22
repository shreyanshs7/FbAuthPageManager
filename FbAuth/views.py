from django.shortcuts import render
from django.views.decorators.http import require_http_methods
import requests
from GrowthPlug.settings import FB_BASE_API
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

fields=["category","name","phone","general_info","about","attire","bio","location","parking","hours","emails","website","description","company_overview","personal_info"]
fieldstring=','.join(fields)

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')


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