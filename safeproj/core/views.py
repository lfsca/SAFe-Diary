from collections import defaultdict
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Ocurrence, SAFeChallenges, Solution
from .forms import RegisterForm, SAFeChallengesForm

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
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


from django.shortcuts import render

def mapa(request):
    return render(request, 'mapa.html')

def register_challenge(request):
    if request.method == 'POST':
        form = SAFeChallengesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('register_challenge')
    else:
        form = SAFeChallengesForm()
    return render(request, 'register_challenge.html', {'form': form})

def challenges_view(request):
    challenges = SAFeChallenges.objects.all()
    ocurrences_by_challenge = defaultdict(list)
    solutions_by_challenge = defaultdict(list)

    for oc in Ocurrence.objects.select_related('user', 'challenge'):
        ocurrences_by_challenge[oc.challenge.id].append(oc)

    for sol in Solution.objects.select_related('author', 'challenge'):
        solutions_by_challenge[sol.challenge.id].append(sol)

    return render(request, 'challenges.html', {
        'challenges': challenges,
        'ocurrences_by_challenge': ocurrences_by_challenge,
        'solutions_by_challenge': solutions_by_challenge,
    })

