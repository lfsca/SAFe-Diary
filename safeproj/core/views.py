from collections import defaultdict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer

from .models import Ocurrence, SAFeChallenges, Solution
from .forms import OcurrenceForm, RegisterForm, SAFeChallengesForm

stemmer = PorterStemmer()


def preprocess(text: str) -> str:
    """Basic tokenization, stemming and stop word removal."""
    tokens = re.findall(r"\b\w+\b", text.lower())
    cleaned = [stemmer.stem(t) for t in tokens if t not in ENGLISH_STOP_WORDS]
    return " ".join(cleaned)

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
            corpus = [preprocess(ch.description) for ch in challenges]
            description_processed = preprocess(description)

            vectorizer = TfidfVectorizer(ngram_range=(1, 2))
            vectors = vectorizer.fit_transform([description_processed] + corpus).toarray()

            similarities = cosine_similarity([vectors[0]], vectors[1:])[0]
            most_similar_index = int(similarities.argmax())
            best_match = challenges[most_similar_index]
            solutions = Solution.objects.filter(challenge=best_match)

    return render(request, "nlp_redirect.html", {
        "user_input": description,
        "best_match": best_match,
        "solutions": solutions
    })