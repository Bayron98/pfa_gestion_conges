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


class TypeConge(models.Model):
    nom = models.CharField(max_length=200)
    def __str__(self):
        return self.nom

class DemandeConge(models.Model):
    employe = models.ForeignKey(Employe, related_name='demandes_conge', on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField()
    type_conge = models.ForeignKey(TypeConge, on_delete=models.CASCADE)
    raison = models.TextField()
    ETAT_CHOICES = [
        ('EN_ATTENTE', 'En attente'),
        ('APPROUVEE', 'Approuvée'),
        ('REFUSEE', 'Refusée'),
    ]
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default='EN_ATTENTE')
    def approuver(self):
        if self.etat != 'APPROUVEE':
            duree_conge = self.duree()
            if self.employe.solde_conge < duree_conge:
                raise ValueError("L'employé n'a pas suffisamment de jours de congé disponibles.")
            self.etat = 'APPROUVEE'
            self.employe.solde_conge -= duree_conge
            self.employe.save()
            self.save()
    def duree(self):
        return (self.date_fin - self.date_debut).days + 1