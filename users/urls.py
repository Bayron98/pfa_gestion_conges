from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Connexion
    path('logout/', views.logout_view, name='logout'),  # Déconnexion
    path('signup/', views.signup_view, name='signup'),  # Inscription
    path('superviseur/dashboard/', views.superviseur_dashboard, name='superviseur_dashboard'),
    path('employe/dashboard/', views.employe_dashboard, name='employe_dashboard'),
    path('ressources_humaines/dashboard/', views.ressources_humaines_dashboard, name='ressources_humaines_dashboard'),
]