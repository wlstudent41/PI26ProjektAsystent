from django.db import models

# Create your models here.
class Egzamin(models.Model):
    przedmiot=models.CharField(max_length=200)
    data=models.DateField("Data egzaminu")
    godzina=models.TimeField("Godzina egzaminu")
    miejsce=models.CharField(max_length=1000)
    typ=models.CharField(max_length=200)

class Porada(models.Model):
    tekst=models.CharField(max_length=1000)
    kategoria=models.CharField(max_length=200)

class Przesad(models.Model):
    tekst=models.CharField(max_length=1000)
    opis=models.CharField(max_length=1000,verbose_name="Opis pochodzenia")


