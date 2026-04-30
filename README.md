# MesaFlow API

API REST completa para gerenciamento de pedidos em restaurante, criada com **FastAPI**.

O projeto foi pensado para portfólio profissional de Back-End, simulando um sistema real usado por garçons, cozinha, bar e administrador.

## Funcionalidades

- Autenticação com JWT
- Controle de usuários e permissões
- Cadastro de mesas
- Pessoas por mesa
- Cardápio com categorias e imagem dos pratos
- Lançamento de pedidos por mesa
- Observações no pedido para cozinha/bar
- Separação por setor: cozinha ou bar
- Alteração de status do pedido
- Previsão de tempo de preparo
- Controle de pagamento
- Ticket médio
- Dashboard administrativo
- Controle básico de estoque
- Alertas de estoque baixo
- Documentação automática Swagger
- Docker Compose com PostgreSQL

## Tecnologias

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / SQLite
- JWT
- Pydantic
- Docker
- Pytest

## Como rodar localmente com SQLite

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Acesse:

```txt
http://127.0.0.1:8000/docs
```

## Como rodar com Docker e PostgreSQL

```bash
docker compose up --build
```

## Usuário administrador inicial

Ao iniciar o projeto, o sistema cria automaticamente:

```txt
Email: admin@mesaflow.com
Senha: admin123
```

## Estrutura

```txt
mesaflow-api/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Objetivo

Demonstrar domínio em criação de APIs REST, regras de negócio, autenticação, banco de dados, arquitetura organizada e documentação profissional.
