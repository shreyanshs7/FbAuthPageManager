from django.shortcuts import render
from django.views.decorators.http import require_http_methods

# Create your views here.
@require_http_methods(['GET'])
def index(request):
    return render(request, 'index.html')

@require_http_methods(['POST'])
def getPageDetails(request):
    # user_access_token = request.POST.get('token', '')
    # response
    pass