from django.db import models
from datetime import datetime

# Create your models here.

class it_liste(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    system = models.CharField(max_length=20)
    gruppe = models.CharField(max_length=40)
    beschreibung = models.CharField(max_length=200)
    code = models.CharField(max_length=300)
    hinweise = models.CharField(max_length=300)

class skripte_db(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    system = models.CharField(max_length=20)
    titel = models.CharField(max_length=40)
    link = models.CharField(max_length=300)
    text_id = models.CharField(max_length=20)
    text = models.TextField()

class roadmap_db(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ziel = models.CharField(max_length=80)
    erledigt = models.BooleanField(default=False)
    erledigt_am = models.DateTimeField(auto_now_add=True)