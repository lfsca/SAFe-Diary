from django.urls import path
from .views import logout_view, challenges_view, home, register, mapa, register_challenge, register_ocurrence, nlp_redirect, suggest_solution, manage_solutions
from django.contrib.auth import views as authviews


urlpatterns = [
    path("", home, name="home"),
    path('register/', register, name='register'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('mapa/', mapa, name='mapa'),
    path('register-challenge/', register_challenge, name='register_challenge'),
    path('challenges/', challenges_view, name='challenges'),
    path('register_ocurrence/', register_ocurrence, name='register_ocurrence'),
    path('search/', nlp_redirect, name='nlp_redirect'),
    path('suggest_solution/', suggest_solution, name='suggest_solution'),
    path('manage_solutions/', manage_solutions, name='manage_solutions'),
]
