
from django.db import models
from django.core.validators import RegexValidator


class Obligation(models.Model):
    nominal = models.FloatField()
    taux_facial = models.FloatField()
    date_valeur = models.DateField()
    maturite = models.FloatField()
    prix_pondere = models.FloatField()

