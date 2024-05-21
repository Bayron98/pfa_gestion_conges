from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Superviseur, Employe, RessourcesHumaines

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if Superviseur.objects.filter(user=user).exists():
                return redirect('superviseur_dashboard')
            elif Employe.objects.filter(user=user).exists():
                return redirect('employe_dashboard')
            elif RessourcesHumaines.objects.filter(user=user).exists():
                return redirect('ressources_humaines_dashboard')
        else:
            return render(request, 'users/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'users/login.html')