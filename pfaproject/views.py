from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from users.models import Superviseur, Employe, RessourcesHumaines

def home(request):
    if request.user.is_authenticated:
        if Superviseur.objects.filter(user=request.user).exists():
            return redirect('superviseur_dashboard')
        elif Employe.objects.filter(user=request.user).exists():
            return redirect('employe_dashboard')
        elif RessourcesHumaines.objects.filter(user=request.user).exists():
            return redirect('ressources_humaines_dashboard')
    else:
        return redirect('login')
