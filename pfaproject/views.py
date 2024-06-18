from django.shortcuts import render, redirect
from users.models import Superviseur, Employe, RessourcesHumaines
from django.http import HttpResponse


# def home(request):
#     if request.user.is_authenticated:
#         if request.user.is_superuser:
#             return HttpResponse("Vous n'êtes pas autorisé à voir cette page.")
#         else:
#             return redirect('dashboard')
#     else:
#         return redirect('login')