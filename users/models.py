from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Equipe(models.Model):
    nom = models.CharField(max_length=100, null=True)
    seuil_conges = models.IntegerField(default=5)

class Superviseur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True)

class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    solde_conge = models.IntegerField(default=0)
    superviseur = models.ForeignKey(Superviseur, on_delete=models.CASCADE)
    equipe = models.ForeignKey(Equipe, on_delete=models.CASCADE, null=True)
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
            raise ValueError(f"L'employé {self.employe.user.first_name} {self.employe.user.last_name} n'a pas suffisamment de jours de congé disponibles.")
        elif DemandeConge.objects.filter(employe__equipe=self.employe.equipe, date_debut__lte=self.date_fin, date_fin__gte=self.date_debut, etat='APPROUVEE').count() >= self.employe.equipe.seuil_conges:
            raise ValueError(f"Le nombre maximum de congés simultanés pour l'équipe {self.employe.equipe.nom} a été atteint.")
        else:
            self.etat = 'APPROUVEE'
            self.employe.solde_conge -= duree_conge
            self.employe.save()
            self.save()
    def duree(self):
        return (self.date_fin - self.date_debut).days + 1