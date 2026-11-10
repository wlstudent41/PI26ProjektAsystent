from django.test import TestCase, Client
from django.urls import reverse
from django.http import JsonResponse
from . import models
import json 
import datetime

# Create your tests here.
class SimpleViewsTests(TestCase):
    def testKalendarz(self):
        response = self.client.get(reverse("kalendarz"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "kalendarz.html")

    def testIndex(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def testPrzesad(self):
        response = self.client.get(reverse("przesad"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "przesady.html")
        self.assertIn("przesady", response.context)

class RandomPoradaTests(TestCase):
    def testEmptyDatabase(self):
        response = self.client.get(reverse("api/randomporada"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Brak porad w bazie")

    def testReturnsPorada(self):
        porada = models.Porada.objects.create(
            tekst="To jest testowa porada",
            kategoria="Testowa"
        )
        response = self.client.get(reverse("api/randomporada"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], porada.id)

class RandomPrzesadTests(TestCase):
    def testEmptyDatabase(self):
        response = self.client.get(reverse("api/randomprzesad"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Brak przesadow w bazie")

    def testReturnsPrzesad(self):
        przesad = models.Przesad.objects.create(
            tekst="Taki jest sobie przesad",
            opis="Ja"
        )

        response = self.client.get(reverse("api/randomprzesad"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["id"], przesad.id)

class ApiPrzesadyTests(TestCase):
    def testGetAllPrzesady(self):
        models.Przesad.objects.create(
            tekst="tak jest",
            opis="z tad"
        )

        response = self.client.get(reverse("api/przesady"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def testWrongMethod(self):
        response = self.client.post(reverse("api/przesady"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), False)

class ApiEgzaminyTests(TestCase):
    def setUp(self):
        self.egzamin = models.Egzamin.objects.create(
            przedmiot="Taki fajny",
            data=datetime.date(2026, 12, 10),
            godzina=datetime.time(10, 0),
            miejsce="Tam za gorami i lasami",
            typ="Pisemny"
        )

    def testGetEgzaminy(self):
        response = self.client.get(reverse("api/egzaminy"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def testFilterPrzedmiot(self):
        response = self.client.get(reverse("api/egzaminy")+"?przedmiot=Taki fajny")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def testFilterWrongPrzedmiot(self):
        response = self.client.get(reverse("api/egzaminy")+"?przedmiot=jakis zly przedmiot")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def testPostEgzamin(self):
        dane = {
            "przedmiot": "Informatyka",
            "data": "2026-12-15",
            "godzina": "12:30",
            "miejsce": "sala 101",
            "typ": "ustny"
        }

        response = self.client.post(reverse("api/egzaminy"), data=json.dumps(dane), content_type="application/json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), True)

        self.assertEqual(models.Egzamin.objects.count(), 2)

        nowy = models.Egzamin.objects.get(przedmiot="Informatyka")
        self.assertEqual(nowy.miejsce, "sala 101")