from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def init(request):
    if request.method == 'GET':
        return HttpResponse("✅ OK >> Model created successfully")
    return HttpResponse(status=405)

