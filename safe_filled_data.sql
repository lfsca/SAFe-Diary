-- Inserção de usuários (simulando stakeholders do SAFe)

INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
    VALUES
    (1, 'pbkdf2_sha256$260000$fakehash$abc123fakehash', NULL, 0, 'ana', 'Ana', 'Silva', 'ana@empresa.com', 0, 1, '2025-07-05T02:10:47.413224'),
    (2, 'pbkdf2_sha256$260000$fakehash$abc123fakehash', NULL, 0, 'bruno', 'Bruno', 'Souza', 'bruno@empresa.com', 0, 1, '2025-07-05T02:10:47.413224'),
    (3, 'pbkdf2_sha256$260000$fakehash$abc123fakehash', NULL, 0, 'carla', 'Carla', 'Mendes', 'carla@empresa.com', 1, 1, '2025-07-05T02:10:47.413224');

-- Desafios relacionados ao SAFe

INSERT INTO core_safechallenges (id, title, description, created_in)
    VALUES
    (1, 'Dificuldade no PI Planning', 'As equipes relatam falta de alinhamento e baixa produtividade durante o PI Planning.', '2025-07-05T02:10:47.413224'),
    (2, 'Resistência à mudança', 'Muitos colaboradores não aderem às práticas SAFe por apego a métodos tradicionais.', '2025-07-05T02:10:47.413224'),
    (3, 'Dependência entre ARTs', 'Falta de sincronização entre ARTs impacta entregas e causa retrabalho.', '2025-07-05T02:10:47.413224');

-- Ocorrências reais relatadas por usuários

INSERT INTO core_ocurrence (id, user_id, challenge_id, occurred_at, notes, status)
    VALUES
    (1, 1, 1, '2024-06-01', 'O planejamento demorou mais de dois dias e gerou retrabalho.', 'accepted'),
    (2, 2, 2, '2024-05-15', 'Equipe sênior recusou as novas práticas propostas.', 'accepted'),
    (3, 1, 3, '2024-06-10', 'Dois ARTs dependiam do mesmo time de infraestrutura sem coordenação.', 'pending');

-- Soluções propostas por usuários

INSERT INTO core_solution (id, challenge_id, author_id, description, created_at, status)
    VALUES
    (1, 1, 2, 'Aplicar treinamentos práticos antes do evento e ter uma agenda clara para o PI Planning.', '2025-07-05T02:10:47.413224', 'accepted'),
    (2, 2, 1, 'Criar uma rede de agentes da mudança para apoiar a transição cultural.', '2025-07-05T02:10:47.413224', 'pending'),
    (3, 3, 2, 'Implementar reuniões quinzenais entre os Release Train Engineers dos ARTs.', '2025-07-05T02:10:47.413224', 'accepted');

-- Avaliações de soluções

INSERT INTO core_solutionevaluation (id, solution_id, user_id, rating, explanation, created_at)
    VALUES
    (1, 1, 1, 5, 'Treinamento realmente ajudou no último planejamento.', '2025-07-05T02:10:47.413224'),
    (2, 3, 1, 4, 'A integração entre RTEs melhorou, mas ainda há atrasos.', '2025-07-05T02:10:47.413224');