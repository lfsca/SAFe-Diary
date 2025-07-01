from collections import defaultdict
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth import logout, login, authenticate

from .models import Ocurrence, SAFeChallenges, Solution
from .forms import OcurrenceForm, RegisterForm, SAFeChallengesForm, SolutionForm
import re
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from nltk.stem import PorterStemmer

def home(request):
    return render(request, "core/home.html")

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         # tenta autenticar o usuário a partir das credenciais
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)                       # aqui passam request e user
#             messages.success(request, "Login realizado com sucesso.")
#             return redirect("home")                    # troque "home" pelo nome da sua URL
#         else:
#             messages.error(request, "Usuário ou senha inválidos.")

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("login")

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
    
stemmer = PorterStemmer()
def preprocess(text: str) -> str:
    
    """Basic tokenization, stemming and stop word removal."""
    tokens = re.findall(r"\b\w+\b", text.lower())
    cleaned = [stemmer.stem(t) for t in tokens if t not in ENGLISH_STOP_WORDS]
    return " ".join(cleaned)

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
    

def suggest_solution(request):
    challenge_id = request.GET.get("challenge_id")
    challenge = get_object_or_404(SAFeChallenges, id=challenge_id)

    if request.method == "POST":
        form = SolutionForm(request.POST)
        if form.is_valid():
            solution = form.save(commit=False)
            solution.author = request.user
            solution.challenge = challenge
            solution.save()
            return redirect("challenges")
    else:
        form = SolutionForm()

    return render(request, "suggest_solution.html", {
        "form": form,
        "challenge": challenge,
    })


def manage_solutions(request):
    if not request.user.is_staff:
        return redirect("login")

    if request.method == "POST":
        solution_id = request.POST.get("solution_id")
        action = request.POST.get("action")
        solution = get_object_or_404(Solution, id=solution_id)

        if action == "accept":
            solution.status = "accepted"
        elif action == "reject":
            solution.status = "rejected"
        elif action == "pend":
            solution.status = "pending"
        solution.save()

        challenge_id = request.POST.get("challenge")
        status = request.POST.get("status")
    else:
        challenge_id = request.GET.get("challenge")
        status = request.GET.get("status")

    challenges = SAFeChallenges.objects.all().order_by("title")

    solutions = []
    if challenge_id and status:
        solutions = Solution.objects.filter(challenge_id=challenge_id, status=status)

    status_choices = Solution.STATUS_CHOICES

    return render(request, "manage_solutions.html", {
        "challenges": challenges,
        "solutions": solutions,
        "selected_challenge": challenge_id,
        "selected_status": status,
        "status_choices": status_choices,
    })