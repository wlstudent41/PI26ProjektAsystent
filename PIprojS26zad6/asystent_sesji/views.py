from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
#loader.get_template('myfirst.html')
import datetime
import json
from django.core import serializers
import random

from . import models


# Create your views here.
def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html lang=\"pl\"><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def kalendarz(request):
    context = {
        'egzaminy' : models.Egzamin.objects.all().values(),
    }
    return render(request, "kalendarz.html", context)
    #return HttpResponse("to jest kalendarz")

#def porada(request):
    #return render(request, "")
    #return HttpResponse("porada na egzamin")

def przesad(request):
    context = {
        'przesady' : models.Przesad.objects.all().values(),
    }
    return render(request, "przesady.html", context)
    #return HttpResponse("tak sie stanie ")

def index(request):
    return render(request, "index.html")

def base(request):
    return render(request, "base.html")

# zwraca jedna losowa porade
def apiRandomPorada(request):
    lastIndex  = models.Porada.objects.count() - 1
    if lastIndex < 0:
        return JsonResponse("Brak porad w bazie", safe=False)
    
    randIndex = random.randint(0, lastIndex)

    allPoradas = models.Porada.objects.all().values()
    porada = allPoradas[randIndex]
    
    return JsonResponse(porada, safe=False)

# zwraca jeden losowy przesad
def apiRandomPrzesad(request):
    lastIndex = models.Przesad.objects.count() - 1
    if lastIndex < 0:
        return JsonResponse("Brak przesadow w bazie", safe=False)

    randIndex = random.randint(0, lastIndex)

    allPrzesady = models.Przesad.objects.all().values()
    przesad = allPrzesady[randIndex]

    return JsonResponse(przesad, safe=False)

# zwraca wszystkie przesady
def apiPrzesady(request):
    if request.method != "GET":
        return JsonResponse(False)

    allPrzesady = models.Przesad.objects.all().values()

    return JsonResponse(list(allPrzesady), safe=False)

#do debugowania
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
# get zwraca liste egzaminow posortowana po dacie (najpierw najblizsze, potem dalsze)
# post tworzy nowy egzamin w bazie
def apiEgzaminy(request):
    print("REQUEST EGZAMINY: " + request.method)
    if request.method == "GET":
        egzaminObjects = models.Egzamin.objects.all()

        # - od najnowszego, bez - od najstarszego
        egzaminObjects = egzaminObjects.order_by("-data")

        egzamins = list(egzaminObjects.values())
        print(egzamins)
        
        return JsonResponse(egzamins, safe=False)

    if request.method == "POST":
        if request.content_type == "application/json": #obsluga danych dla json
            dane = json.loads(request.body)
        elif request.content_type == "application/x-www-form-urlencoded": #obsluga danych dla url encoded
            dane = request.POST
        else:
            return JsonResponse(False, safe=False) # nie obslugujemy innych sry bye
        
        
        ePrzedmiot = dane.get("przedmiot", "programowanie internetowe")
        eData = dane.get("data", datetime.date.today())
        eGodzina = dane.get("godzina", datetime.datetime.now().time())
        eMiejsce = dane.get("miejsce", "tu i teraz")
        eTyp = dane.get("typ", "pisemny")

        print(ePrzedmiot, eData, eGodzina, eMiejsce, eTyp)

        nowyEgzamin = models.Egzamin(przedmiot=ePrzedmiot,data=eData,godzina=eGodzina,miejsce=eMiejsce,typ=eTyp)
        nowyEgzamin.save()

        return JsonResponse(True, safe=False)