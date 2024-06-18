from django.contrib import admin

# Register your models here.
from .models import Employe, RessourcesHumaines, Superviseur, DemandeConge, TypeConge

admin.site.register(Employe)
admin.site.register(RessourcesHumaines)
admin.site.register(Superviseur)
admin.site.register(DemandeConge)
admin.site.register(TypeConge)