from django.db import models
from django.contrib.auth.models import User

class SAFeChallenges(models.Model):
    titles = [
        ('planning', 'Planning'),
        ('resistence', 'Resistence to Change'),
        ('complexity', 'Framework Complexity'),
        ('communication', 'Communication'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=30, choices=titles)
    description = models.TextField()
    created_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_titleo_display()} - {self.created_in.strftime('%d/%m/%Y')}"

class Ocurrence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges')
    challenge = models.ForeignKey(SAFeChallenges, on_delete=models.CASCADE, related_name='ocurrences')
    occurred_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.challenge.get_title_display()} on {self.occurred_at.strftime('%d/%m/%Y')}"

class Solution(models.Model):
    challenge = models.ForeignKey(SAFeChallenges, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solução por {self.author.username} para {self.challenge}"