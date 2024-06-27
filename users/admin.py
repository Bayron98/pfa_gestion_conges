from django.contrib import admin

# Register your models here.
from .models import Employe, RessourcesHumaines, Superviseur, DemandeConge, TypeConge, Equipe

admin.site.register(Equipe)
admin.site.register(Employe)
admin.site.register(RessourcesHumaines)
admin.site.register(Superviseur)
admin.site.register(DemandeConge)
admin.site.register(TypeConge)