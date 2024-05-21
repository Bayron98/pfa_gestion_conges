from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Superviseur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solde_conge = models.IntegerField(default=0)
    superviseur = models.ForeignKey(Superviseur, on_delete=models.CASCADE)

class RessourcesHumaines(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

