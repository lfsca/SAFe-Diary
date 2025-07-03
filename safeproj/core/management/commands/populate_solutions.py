from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import SAFeChallenges, Solution  # Altere 'core' se necessário
import random

class Command(BaseCommand):
    help = 'Popula o banco com soluções realistas para os desafios do SAFe.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=3,
            help='Número de soluções por desafio (padrão: 3)'
        )
        parser.add_argument(
            '--status',
            type=str,
            default='approved',
            help='Status das soluções (approved, pending, rejected, etc.)'
        )

    def handle(self, *args, **options):
        count_per_challenge = options['count']
        status = options['status']

        author = User.objects.filter(is_staff=True).first() or User.objects.first()

        if not author:
            print("YAI")
            self.stdout.write(self.style.ERROR(" Nenhum usuário encontrado. Crie um com createsuperuser."))
            return

        solutions_map = {
            "Resistance": [
                "Promover workshops de cultura ágil com liderança.",
                "Compartilhar casos de sucesso internos com SAFe.",
                "Incluir os líderes no planejamento do PI Planning."
            ],
            "Complexity": [
                "Mapear dependências entre ARTs usando visual boards.",
                "Simplificar papéis com orientações visuais claras.",
                "Adotar ferramentas que integram backlog e dependências."
            ],
            "Communication": [
                "Criar uma cerimônia semanal de alinhamento entre POs.",
                "Usar canais dedicados para comunicação inter-ARTs.",
                "Promover eventos de team-building entre ARTs."
            ],
            "Planning": [
                "Preparar o backlog do PI com semanas de antecedência.",
                "Realizar PI Planning com partes assíncronas.",
                "Usar checklists visuais para validar escopo e dependências."
            ],
            "Excesso de Cerimônias": [
                "Coletar feedback trimestral sobre o valor das cerimônias.",
                "Consolidar reuniões quando possível.",
                "Eliminar cerimônias com baixo ROI e pouco engajamento."
            ],
            "Dificuldade de Medir Valor Entregue": [
                "Estabelecer OKRs mensuráveis por ART.",
                "Criar dashboards com métricas de negócio e entrega.",
                "Revisar entregas com foco no impacto ao usuário final."
            ],
            "Falta de Flexibilidade e Adaptação": [
                "Permitir ajustes no framework sem perder os princípios centrais.",
                "Avaliar o uso de SAFe de forma evolutiva.",
                "Documentar adaptações aprovadas e seus resultados."
            ],
            "Falta de Investimento em Capacitação Contínua": [
                "Criar trilhas de aprendizado por papel.",
                "Oferecer treinamentos regulares internos sobre SAFe.",
                "Apoiar certificações com subsídio ou bolsas."
            ]
        }

        total = 0
        print("IAAIIII")
        for title, base_descs in solutions_map.items():
            self.stdout.write(f"Tentando encontrar desafio: '{title}'")
            try:
                challenge = SAFeChallenges.objects.get(title__iexact=title.strip())
                print("OPAAAAA")
                print(challenge)
                self.stdout.write(self.style.SUCCESS(f"✅ Desafio encontrado: {challenge.title}"))

                for i in range(count_per_challenge):
                    desc = random.choice(base_descs)
                    Solution.objects.create(
                        challenge=challenge,
                        description=desc,
                        author=author,
                        status=status
                    )
                    total += 1
            except SAFeChallenges.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"❌ Desafio não encontrado no banco: '{title}'"))
