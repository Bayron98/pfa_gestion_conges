from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),  # Connexion
    path('logout/', views.logout_view, name='logout'),  # Déconnexion
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create/', views.create, name='create'),
    path('accepter/<int:id>/', views.accepter, name='accepter'),
    path('refuser/<int:id>/', views.refuser, name='refuser'),
    path('security/', views.security, name='security'),
    path('conges/settings/', views.settings, name='settings'),
    path('modify/<int:id>/<str:model>/', views.modify, name='modify'),
    path('delete/<int:id>/<str:model>/', views.delete, name='delete'),
    # path('superviseur/dashboard/', views.superviseur_dashboard, name='superviseur_dashboard'),
    # path('employe/dashboard/', views.employe_dashboard, name='employe_dashboard'),
    # path('ressources_humaines/dashboard/', views.ressources_humaines_dashboard, name='ressources_humaines_dashboard'),
]