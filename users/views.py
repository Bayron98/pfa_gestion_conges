from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Superviseur, Employe, RessourcesHumaines

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Nom d\'utilisateur ou mot de passe incorrect.'})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/login.html')
    
def logout_view(request):
    logout(request)
    return redirect('login')
def dashboard_view(request):
    if request.user.is_authenticated:
        if Superviseur.objects.filter(user=request.user).exists():
            return render(request, 'users/superviseur_dashboard.html')
        elif Employe.objects.filter(user=request.user).exists():
            return render(request, 'users/employe_dashboard.html')
        elif RessourcesHumaines.objects.filter(user=request.user).exists():
            return render(request, 'users/ressources_humaines_dashboard.html')
        else:
            return render(request, 'users/dashboard.html')
    else:
        return redirect('login')