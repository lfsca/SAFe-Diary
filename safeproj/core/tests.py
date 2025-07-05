from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch

from .forms import RegisterForm
from .models import SAFeChallenges, Ocurrence, Solution, SolutionEvaluation, StatusChoices
from .services import StatusTransitionService
from django.contrib.messages import get_messages


class RegisterFormTests(TestCase):
    def test_password_mismatch(self):
        form = RegisterForm(data={
            'username': 'john',
            'email': 'john@example.com',
            'password': 'pass1',
            'confirm_password': 'pass2',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('As senhas não coincidem.', form.errors['__all__'])


class StatusTransitionServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('u', password='pass')
        self.challenge = SAFeChallenges.objects.create(title='t', description='d')

    def test_update_changes_status(self):
        oc = Ocurrence.objects.create(
            user=self.user,
            challenge=self.challenge,
            occurred_at='2024-01-01',
        )
        service = StatusTransitionService()
        service.update(oc, 'accept')
        oc.refresh_from_db()
        self.assertEqual(oc.status, StatusChoices.ACCEPTED)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('user', password='pwd')
        self.staff = User.objects.create_user('staff', password='pwd', is_staff=True)
        self.challenge = SAFeChallenges.objects.create(title='c1', description='d1')

    def test_home_view(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_register_view_creates_user(self):
        resp = self.client.post(reverse('register'), {
            'username': 'new',
            'email': 'new@example.com',
            'password': 'pwd',
            'confirm_password': 'pwd',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='new').exists())

    def test_register_challenge_post(self):
        resp = self.client.post(reverse('register_challenge'), {
            'title': 'c2',
            'description': 'dd',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(SAFeChallenges.objects.filter(title='c2').exists())

    def test_create_challenge_requires_staff(self):
        self.client.login(username='user', password='pwd')
        resp = self.client.get(reverse('create_challenge'))
        self.assertEqual(resp.status_code, 302)  # redirected for non staff

        self.client.logout()
        self.client.login(username='staff', password='pwd')
        resp = self.client.get(reverse('create_challenge'))
        self.assertEqual(resp.status_code, 200)

    def test_register_ocurrence_post(self):
        self.client.login(username='user', password='pwd')
        resp = self.client.post(reverse('register_ocurrence') + f'?challenge_id={self.challenge.id}', {
            'occurred_at': '2024-01-01',
            'notes': 'something',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Ocurrence.objects.filter(user=self.user, challenge=self.challenge).exists())

    @patch('core.views.ChallengeMatcher')
    def test_nlp_redirect_post_uses_matcher(self, mock_matcher):
        mock_matcher.return_value.find_best_match.return_value = (self.challenge, [])
        resp = self.client.post(reverse('nlp_redirect'), {'description': 'desc'})
        self.assertEqual(resp.status_code, 200)
        mock_matcher.return_value.find_best_match.assert_called_once_with('desc')

    def test_suggest_solution_post(self):
        self.client.login(username='user', password='pwd')
        resp = self.client.post(reverse('suggest_solution') + f'?challenge_id={self.challenge.id}', {
            'description': 'solution',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Solution.objects.filter(author=self.user, challenge=self.challenge).exists())
        
        
class EvaluateSolutionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user', password='pwd')
        self.challenge = SAFeChallenges.objects.create(title='Desafio 1', description='Desc')
        self.solution = Solution.objects.create(
            challenge=self.challenge,
            author=self.user,
            description='Solução exemplo',
            status=StatusChoices.ACCEPTED
        )
        self.url = reverse('evaluate_solution') + f'?solution_id={self.solution.id}'

    def test_get_evaluation_form(self):
        self.client.login(username='user', password='pwd')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        self.assertEqual(response.context['solution'], self.solution)

    def test_post_valid_evaluation_creates_object(self):
        self.client.login(username='user', password='pwd')
        response = self.client.post(self.url, {
            'rating': 5,
            'explanation': 'Muito útil!',
        }, follow=True)

        self.assertRedirects(response, reverse('challenges'))
        self.assertTrue(SolutionEvaluation.objects.filter(user=self.user, solution=self.solution).exists())

        # Verifica se a mensagem de sucesso foi exibida
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Avaliação registrada!", [msg.message for msg in messages])

    def test_reject_evaluation_for_non_accepted_solution(self):
        self.solution.status = StatusChoices.PENDING
        self.solution.save()

        self.client.login(username='user', password='pwd')
        url = reverse('evaluate_solution') + f'?solution_id={self.solution.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)  # get_object_or_404 deve impedir acesso