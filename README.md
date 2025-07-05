# SAFe Diary

Este projeto é uma aplicação web desenvolvida com Django, voltada para o registro, análise e colaboração em torno dos desafios enfrentados na adoção do framework SAFe (Scaled Agile Framework) em grandes organizações.

## Funcionalidades

- Cadastro e autenticação de usuários
- Registro de desafios relacionados à implementação do SAFe
- Submissão de ocorrências reais vinculadas a desafios
- Propostas de soluções por parte da comunidade
- Avaliação colaborativa das soluções sugeridas
- Busca inteligente por desafio via NLP (processamento de linguagem natural)

## Estrutura do Projeto

O projeto segue a estrutura típica de um aplicativo Django modular:

### Principais Arquivos e Diretórios

- `safeproj/core/models.py`  
  Contém os modelos de domínio: `SAFeChallenges`, `Ocurrence`, `Solution`, `SolutionEvaluation` e o enumerador `StatusChoices`.

- `safeproj/core/forms.py`  
  Centraliza os formulários utilizados nas views.

- `safeproj/core/services.py`  
  Implementa regras de negócio reutilizáveis.

- `safeproj/core/views.py`  
  Define as views que lidam com requisições, autenticação, renderização de templates e integração com os serviços.

- `safeproj/core/tests.py`  
  Contém testes automatizados para formulários, serviços e views usando `TestCase` e `Client`.

- `safeproj/templates/`  
  Armazena os templates HTML usados nas páginas da aplicação.

- `safeproj/static/`  
  Contém os arquivos estáticos como CSS e JS.

- `safeproj/urls.py`  
  Roteamento principal do projeto.

- safe_filled_data.sql contém dados simulados de usuários, desafios, ocorrências, soluções e avaliações, prontos para popular o banco de dados.

- `manage.py`  
  Script utilitário para comandos administrativos do Django.

## Instalação

1. Clone o repositório:

   ```bash
   git clone git@github.com:lfsca/SAFe-Diary.git
   cd safeproj

2. Crie um ambiente virtual:

	```bash
	python -m venv venv
	source venv/bin/activate  # Linux/macOS
	venv\Scripts\activate     # Windows

3. Instale as dependências:

	```bash
	pip install -r requirements.txt

4. Aplique as migrações:

	```bash
	python manage.py migrate

5. Execute o servidor:

	```bash
	python manage.py runserver

6. Criar Usuário Administrador (Importante para testar todas as funcionalidades):

	```bash
	python manage.py shell

		
	from django.contrib.auth.models import User
	User.objects.create_user(username='carla', password='123', is_staff=True)


(Opcional) Executar testes automatizados:

	```bash
	python manage.py test
