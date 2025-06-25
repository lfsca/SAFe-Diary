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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    challenge = models.ForeignKey('SAFeChallenges', on_delete=models.CASCADE)
    occurred_at = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.challenge} - {self.user} em {self.occurred_at}"

class Solution(models.Model):
    challenge = models.ForeignKey(SAFeChallenges, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solução por {self.author.username} para {self.challenge}"