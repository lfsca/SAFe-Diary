from django.urls import path
from .views import home, register, mapa, registrar_desafio, desafio_sucesso
from django.contrib.auth import views as authviews


urlpatterns = [
    path("", home, name="home"),
    path('register/', register, name='register'),
    path('login/', authviews.LoginView.as_view(), name='login'),
    path('logout/', authviews.LogoutView.as_view(next_page='login'), name='logout'),
    path('mapa/', mapa, name='mapa'),
    path('registrar-desafio/', registrar_desafio, name='registrar_desafio'),
    path('desafio-sucesso/', desafio_sucesso, name='desafio_sucesso'),
]
