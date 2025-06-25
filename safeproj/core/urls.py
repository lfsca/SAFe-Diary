from django.urls import path
from .views import challenges_view, home, register, mapa, register_challenge
from django.contrib.auth import views as authviews


urlpatterns = [
    path("", home, name="home"),
    path('register/', register, name='register'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(next_page='login'), name='logout'),
    path('mapa/', mapa, name='mapa'),
    path('register-challenge/', register_challenge, name='register_challenge'),
    path('challenges/', challenges_view, name='challenges'),
]
