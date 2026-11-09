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
    return render(request, "kalendarz.html")
    #return HttpResponse("to jest kalendarz")

#def porada(request):
    #return render(request, "")
    #return HttpResponse("porada na egzamin")

def przesad(request):
    return render(request, "przesady.html")
    #return HttpResponse("tak sie stanie ")

def index(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")