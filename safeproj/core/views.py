from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RegisterForm, SAFeChallangesForm

# Create your views here.

def home(request):
    return render(request, "core/home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Conta criada com sucesso!")
            return redirect("login")  # ou onde preferir
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


from django.shortcuts import render

def mapa(request):
    return render(request, 'mapa.html')

def registrar_desafio(request):
    if request.method == 'POST':
        form = SAFeChallangesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('desafio_sucesso')
    else:
        form = SAFeChallangesForm()
    return render(request, 'registrar_desafio.html', {'form': form})

def desafio_sucesso(request):
    return render(request, 'desafio_sucesso.html')
