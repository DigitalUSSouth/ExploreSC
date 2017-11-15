#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import urllib as ul


def index(request):
    query = request.GET['q']
    with ul.request.urlopen('https://www.digitalussouth.org/api?q='+query+'&start=0') as response:
        html = response.read()
    response = html
    return HttpResponse(response)

