from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
#loader.get_template('myfirst.html')
import datetime


# Create your views here.
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html lang=\"pl\"><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def kalendarz(request):
    return HttpResponse("to jest kalendarz")

def porada(request):
    return HttpResponse("porada na egzamin")

def przesad(request):
    return HttpResponse("tak sie stanie ")
