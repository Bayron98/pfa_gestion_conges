from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Superviseur, Employe, RessourcesHumaines, DemandeConge
from django.http import HttpResponse
from .forms import DemandeCongeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard_view(request):
        if Superviseur.objects.filter(user=request.user).exists():
            return superviseur_index(request)
        elif Employe.objects.filter(user=request.user).exists():
            return employe_index(request)
        elif RessourcesHumaines.objects.filter(user=request.user).exists():
            return ressourceshumaines_index(request)
        else:
            return HttpResponse("Vous n'êtes pas autorisé à voir cette page.")


def employe_index(request):
    employe = Employe.objects.get(user=request.user)
    demandes_conge = DemandeConge.objects.filter(employe=employe)
    context = {
        'employe': employe,
        'demandes_conge': demandes_conge,
    }
    return render(request, 'employes/index.html', context)

def superviseur_index(request):
    superviseur = Superviseur.objects.get(user=request.user)
    employes = Employe.objects.filter(superviseur=superviseur)
    
    demandes_conge_en_attente = DemandeConge.objects.filter(employe__in=employes, etat='EN_ATTENTE')
    demandes_conge_approuvees = DemandeConge.objects.filter(employe__in=employes, etat='APPROUVEE')
    demandes_conge_refusees = DemandeConge.objects.filter(employe__in=employes, etat='REFUSEE')

    context = {
        'superviseur': superviseur,
        'employes': employes,
        'demandes_conge_en_attente': demandes_conge_en_attente,
        'demandes_conge_approuvees': demandes_conge_approuvees,
        'demandes_conge_refusees': demandes_conge_refusees,
    }
    return render(request, 'superviseurs/index.html', context)

def accepter(request, id):
    demande = get_object_or_404(DemandeConge, id=id)
    try:
        demande.approuver()
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('dashboard')

def refuser(request, id):
    demande = get_object_or_404(DemandeConge, id=id)
    demande.etat = 'REFUSEE'
    demande.save()
    return redirect('dashboard')

@login_required   
def create(request):
    if request.method == 'POST':
        form = DemandeCongeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.employe = Employe.objects.get(user=request.user)
            if DemandeConge.objects.filter(employe=demande.employe, date_debut__lte=demande.date_fin, date_fin__gte=demande.date_debut).exists():
                form.add_error(None, "Une demande de congé pour les mêmes dates existe déjà.")
            elif demande.duree() > demande.employe.solde_conge:
                form.add_error(None, "La durée de la demande de congé est supérieure à votre solde de congé.")
            else:
                demande.save()
                return redirect('dashboard')
    else:
        form = DemandeCongeForm()
    return render(request, 'employes/create.html', {'form': form})




def ressourceshumaines_index(request):
    pass

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse("Vous n'êtes pas autorisé à voir cette page.")
        else:
            return redirect('dashboard')
    else:
        return redirect('login')