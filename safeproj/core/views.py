from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .forms import OcurrenceForm, RegisterForm, SAFeChallengesForm, SolutionForm
from .models import Ocurrence, SAFeChallenges, Solution, STATUS_CHOICES
from .services import ChallengeMatcher, StatusTransitionService


def home(request):
    return render(request, "core/home.html")

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
        ch.id: Ocurrence.objects.filter(challenge=ch, status="accepted") for ch in challenges
    }

    # Organiza soluções por challenge ID
    solutions_by_challenge = {
        ch.id: Solution.objects.filter(challenge=ch, status = "accepted") for ch in challenges
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
            matcher = ChallengeMatcher()
            best_match, solutions = matcher.find_best_match(description)

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


def manage(request):
    if not request.user.is_staff:
        return redirect("login")

    status_service = StatusTransitionService()

    if request.method == "POST":
        item_type = request.POST.get("type")
        item_id = request.POST.get("item_id")
        action = request.POST.get("action")

        if item_type == "solution":
            item = get_object_or_404(Solution, id=item_id)
        else:
            item = get_object_or_404(Ocurrence, id=item_id)

        status_service.update(item, action)

        item_type = request.POST.get("type")
        challenge_id = request.POST.get("challenge")
        status = request.POST.get("status")
    else:
        item_type = request.GET.get("type")
        challenge_id = request.GET.get("challenge")
        status = request.GET.get("status")

    challenges = SAFeChallenges.objects.all().order_by("title")

    items = []
    if item_type and challenge_id and status:
        Model = Solution if item_type == "solution" else Ocurrence
        items = Model.objects.filter(challenge_id=challenge_id, status=status)

    status_choices = STATUS_CHOICES

    return render(request, "manage.html", {
        "challenges": challenges,
        "items": items,
        "selected_challenge": challenge_id,
        "selected_status": status,
        "status_choices": status_choices,
        "selected_type": item_type,
    })