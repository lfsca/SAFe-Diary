from collections import defaultdict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .models import Ocurrence, SAFeChallenges, Solution
from .forms import OcurrenceForm, RegisterForm, SAFeChallengesForm

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

    # Organiza ocorrências por challenge ID
    ocurrences_by_challenge = {
        ch.id: Ocurrence.objects.filter(challenge=ch) for ch in challenges
    }

    # Organiza soluções por challenge ID
    solutions_by_challenge = {
        ch.id: Solution.objects.filter(challenge=ch) for ch in challenges
    }

    return render(request, 'challenges.html', {
        'challenges': challenges,
        'ocurrences_by_challenge': ocurrences_by_challenge,
        'solutions_by_challenge': solutions_by_challenge,
    })

def register_ocurrence(request):
    challenge_id = request.GET.get('challenge_id')
    challenge = get_object_or_404(SAFeChallenges, id=challenge_id)

    if request.method == 'POST':
        form = OcurrenceForm(request.POST)
        if form.is_valid():
            ocurrence = form.save(commit=False)
            ocurrence.user = request.user
            ocurrence.challenge = challenge
            ocurrence.save()
            return redirect('challenges')
    else:
        form = OcurrenceForm()

    return render(request, 'register_ocurrence.html', {
        'form': form,
        'challenge': challenge
    })

def nlp_redirect(request):
    best_match = None
    solutions = None
    description = ""

    if request.method == "POST":
        description = request.POST.get("description", "").strip()

        if description:
            challenges = SAFeChallenges.objects.all()
            corpus = [ch.description for ch in challenges]

            vectorizer = TfidfVectorizer().fit_transform([description] + corpus)
            vectors = vectorizer.toarray()

            similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
            most_similar_index = int(similarities.argmax())
            best_match = challenges[most_similar_index]
            solutions = Solution.objects.filter(challenge=best_match)

    return render(request, "nlp_redirect.html", {
        "user_input": description,
        "best_match": best_match,
        "solutions": solutions
    })