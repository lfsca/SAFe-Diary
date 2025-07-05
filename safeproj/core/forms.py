from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Ocurrence, SAFeChallenges, Solution, SolutionEvaluation

class RegisterForm(forms.ModelForm):
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirmar Senha", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("As senhas não coincidem.")

class SAFeChallengesForm(forms.ModelForm):
    class Meta:
        model = SAFeChallenges
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'title': 'Type of Challenge',
            'description': 'Detailed Description',
        }

class OcurrenceForm(forms.ModelForm):
    class Meta:
        model = Ocurrence
        fields = ['occurred_at', 'notes']
        widgets = {
            'occurred_at': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descreva o que aconteceu...'}),
        }
        labels = {
            'occurred_at': 'Data da Ocorrência',
            'notes': 'Notas (opcional)',
        }
        
class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your solution...'}),
        }
        labels = {
            'description': 'Solution',
        }


class SolutionEvaluationForm(forms.ModelForm):
    class Meta:
        model = SolutionEvaluation
        fields = ['rating', 'explanation']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'rating': 'Nota (1-5)',
            'explanation': 'Explicação',
        }