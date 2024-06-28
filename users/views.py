from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Superviseur, Employe, RessourcesHumaines, DemandeConge, TypeConge, Equipe
from django.http import HttpResponse
from .forms import DemandeCongeForm, TypeCongeForm, EquipeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Count
from django.db.models import Avg
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.core.paginator import Paginator


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
            return redirect('admin:index')


def employe_index(request):
    employe = Employe.objects.get(user=request.user)
    demandes_conge = DemandeConge.objects.filter(employe=employe)

    paginator = Paginator(demandes_conge, 5)

    page_number = request.GET.get('page')

    demandes_conge_page = paginator.get_page(page_number)
    nombre_demandes_conge = paginator.count
    context = {
        'employe': employe,
        'demandes_conge': demandes_conge_page,
        'nombre_demandes_conge': nombre_demandes_conge,
    }
    return render(request, 'employes/index.html', context)

def superviseur_index(request):
    superviseur = Superviseur.objects.get(user=request.user)
    employes = Employe.objects.filter(superviseur=superviseur)
    
    demandes_conge_en_attente = DemandeConge.objects.filter(employe__in=employes, etat='EN_ATTENTE')
    demandes_conge_approuvees = DemandeConge.objects.filter(employe__in=employes, etat='APPROUVEE')
    demandes_conge_refusees = DemandeConge.objects.filter(employe__in=employes, etat='REFUSEE')

    paginator = Paginator(demandes_conge_en_attente, 5)  # Affiche 5 objets par page
    page_number = request.GET.get('page_attente')
    demandes_conge_en_attente = paginator.get_page(page_number)
    nombre_demandes_conge_en_attente = paginator.count

    paginator = Paginator(demandes_conge_approuvees, 5)  # Affiche 5 objets par page
    page_number = request.GET.get('page_approuvees')
    demandes_conge_approuvees = paginator.get_page(page_number)
    nombre_demandes_conge_approuvees = paginator.count

    paginator = Paginator(demandes_conge_refusees, 5)  # Affiche 5 objets par page
    page_number = request.GET.get('page_refusees')
    demandes_conge_refusees = paginator.get_page(page_number)
    nombre_demandes_conge_refusees = paginator.count

    context = {
        'superviseur': superviseur,
        'employes': employes,
        'demandes_conge_en_attente': demandes_conge_en_attente,
        'demandes_conge_approuvees': demandes_conge_approuvees,
        'demandes_conge_refusees': demandes_conge_refusees,
        'nombre_demandes_conge_approuvees': nombre_demandes_conge_approuvees,
        'nombre_demandes_conge_en_attente': nombre_demandes_conge_en_attente,
        'nombre_demandes_conge_refusees': nombre_demandes_conge_refusees,
    }
    return render(request, 'superviseurs/index.html', context)

# def ressourceshumaines_index(request):
#     ressourceshumaines = RessourcesHumaines.objects.get(user=request.user)
#     employes = Employe.objects.all()
#     demandes_conge_en_attente = DemandeConge.objects.filter(etat='EN_ATTENTE')
#     demandes_conge_approuvees = DemandeConge.objects.filter(etat='APPROUVEE')
#     demandes_conge_refusees = DemandeConge.objects.filter(etat='REFUSEE')
#     context = {
#         'ressourceshumaines': ressourceshumaines,
#         'employes': employes,
#         'demandes_conge_en_attente': demandes_conge_en_attente,
#         'demandes_conge_approuvees': demandes_conge_approuvees,
#         'demandes_conge_refusees': demandes_conge_refusees,
#     }
#     return render(request, 'ressourceshumaines/index.html', context)

from django.core.paginator import Paginator

def ressourceshumaines_index(request):
    ressourceshumaines = RessourcesHumaines.objects.get(user=request.user)

    paginator_employes = Paginator(Employe.objects.all(), 5)
    paginator_en_attente = Paginator(DemandeConge.objects.filter(etat='EN_ATTENTE'), 5)
    paginator_approuvees = Paginator(DemandeConge.objects.filter(etat='APPROUVEE'), 5)
    paginator_refusees = Paginator(DemandeConge.objects.filter(etat='REFUSEE'), 5)

    page_number_employes = request.GET.get('page_employes')
    page_number_en_attente = request.GET.get('page_en_attente')
    page_number_approuvees = request.GET.get('page_approuvees')
    page_number_refusees = request.GET.get('page_refusees')

    employes_page = paginator_employes.get_page(page_number_employes)
    en_attente_page = paginator_en_attente.get_page(page_number_en_attente)
    approuvees_page = paginator_approuvees.get_page(page_number_approuvees)
    refusees_page = paginator_refusees.get_page(page_number_refusees)

    nombre_demandes_conge_en_attente = DemandeConge.objects.filter(etat='EN_ATTENTE').count()
    nombre_demandes_conge_approuvees = DemandeConge.objects.filter(etat='APPROUVEE').count()
    nombre_demandes_conge_refusees = DemandeConge.objects.filter(etat='REFUSEE').count()

    context = {
        'ressourceshumaines': ressourceshumaines,
        'employes': employes_page,
        'demandes_conge_en_attente': en_attente_page,
        'demandes_conge_approuvees': approuvees_page,
        'demandes_conge_refusees': refusees_page,
        'nombre_demandes_conge_en_attente': nombre_demandes_conge_en_attente,
        'nombre_demandes_conge_approuvees': nombre_demandes_conge_approuvees,
        'nombre_demandes_conge_refusees': nombre_demandes_conge_refusees,
    }
    return render(request, 'ressourceshumaines/index.html', context)

@login_required   
def accepter(request, id):
    demande = get_object_or_404(DemandeConge, id=id)
    try:
        demande.approuver()
        envoyer_notification_email(demande)
    except ValueError as e:
        messages.error(request, str(e))

    return redirect('dashboard')
@login_required   
def refuser(request, id):
    demande = get_object_or_404(DemandeConge, id=id)
    demande.etat = 'REFUSEE'
    envoyer_notification_email(demande)
    demande.save()
    return redirect('dashboard')



@login_required
def security(request):
    if Superviseur.objects.filter(user=request.user).exists():
        return security_superviseur(request)
    if RessourcesHumaines.objects.filter(user=request.user).exists():
        return security_ressourceshumaines(request)
    else:
        return security_employe(request)
def security_superviseur(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'superviseurs/security.html', {'form': form})

def security_employe(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'employes/security.html', {'form': form})

def security_ressourceshumaines(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user) 
            return redirect('dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'ressourceshumaines/security.html', {'form': form})

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


def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return HttpResponse("Vous n'êtes pas autorisé à voir cette page.")
        else:
            return redirect('dashboard')
    else:
        return redirect('login')
    
@login_required   
def settings(request):
    equipes = Equipe.objects.all()
    types_conge = TypeConge.objects.all()

    context = {
        'equipes': equipes,
        'types_conge': types_conge,
    }

    return render(request, 'ressourceshumaines/settings.html', context)

@login_required   
def modify(request, id, model):
    model_class = globals()[model]
    instance = get_object_or_404(model_class, id=id)

    if model == 'Equipe':
        form_class = EquipeForm
    elif model == 'TypeConge':
        form_class = TypeCongeForm

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
        'model': model,
    }

    return render(request, 'ressourceshumaines/modify.html', context)
@login_required   
def delete(request, id, model):
    model_class = globals()[model]
    instance = get_object_or_404(model_class, id=id)
    instance.delete()
    return redirect('settings')




@login_required
def reporting(request):
    # Obtenir le nombre de demandes de congé par état
    demandes_conge_par_etat = DemandeConge.objects.values('etat').annotate(nombre=Count('etat'))
    etat_display_mapping = dict(DemandeConge.ETAT_CHOICES)
    for item in demandes_conge_par_etat:
        item['etat_display'] = etat_display_mapping[item['etat']]

    # Obtenir le solde de congé moyen par équipe
    solde_conge_moyen_par_equipe = Employe.objects.values('equipe__nom').annotate(solde_conge_moyen=Avg('solde_conge'))

    # Obtenir la répartition des types de congés
    types_conges = TypeConge.objects.values('nom')
    nombre_conges_par_type = DemandeConge.objects.values('type_conge__nom').annotate(nombre=Count('type_conge'))


    demandes_conge_approuvees_par_equipe = DemandeConge.objects.filter(etat='APPROUVEE').values('employe__equipe__nom').annotate(nombre=Count('employe__equipe'))
    # Obtenir l'historique des congés
    historique_conges = DemandeConge.objects.filter(etat='APPROUVEE').values('date_debut').annotate(nombre_conges=Count('id')).order_by('date_debut')

    context = {
        'demandes_conge_par_etat': demandes_conge_par_etat,
        'solde_conge_moyen_par_equipe': solde_conge_moyen_par_equipe,
        'types_conges': types_conges,
        'nombre_conges_par_type': nombre_conges_par_type,
        'demandes_conge_approuvees_par_equipe': demandes_conge_approuvees_par_equipe,
        'historique_conges': historique_conges,
    }
    return render(request, 'ressourceshumaines/reporting.html', context)






from sib_api_v3_sdk import SendSmtpEmail, ApiClient, Configuration, SendSmtpEmailTo
from sib_api_v3_sdk.api.transactional_emails_api import TransactionalEmailsApi
from babel.dates import format_date


def envoyer_notification_email(demande):
    configuration = Configuration()
    configuration.api_key['api-key'] = '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' 

    api_client = ApiClient(configuration)
    api_instance = TransactionalEmailsApi(api_client)

    date_debut = format_date(demande.date_debut, format='long', locale='fr')
    date_fin = format_date(demande.date_fin, format='long', locale='fr')

    sujet = f"Etat de votre demande de congé : {demande.get_etat_display()}"
    message = f"Votre demande de congé pour la période du {date_debut} au {date_fin} a été {demande.get_etat_display()}."

    email = SendSmtpEmail(
        to=[SendSmtpEmailTo(email=demande.employe.user.email)],
        sender=SendSmtpEmailTo(email='badrbayour@gmail.com'), 
        subject=sujet,
        html_content=message
    )

    api_instance.send_transac_email(email)