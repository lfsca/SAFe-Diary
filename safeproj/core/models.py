from django.db import models
from django.contrib.auth.models import User


class StatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    REJECTED = "rejected", "Rejected"

class SAFeChallenges(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.created_in.strftime('%d/%m/%Y')}"

class Ocurrence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey('SAFeChallenges', on_delete=models.CASCADE)
    occurred_at = models.DateField()
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return f"{self.challenge} - {self.user} em {self.occurred_at}"

class Solution(models.Model):
    
    challenge = models.ForeignKey(SAFeChallenges, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING)

    def __str__(self):
        return f"Solução por {self.author.username} para {self.challenge}"


class SolutionEvaluation(models.Model):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="evaluations")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("solution", "user")

    def __str__(self):
        return f"{self.user.username} avaliou {self.solution} com {self.rating}"
