# Docker Compose Multi-Service Playground

Este projeto demonstra como orquestrar três serviços dependentes com Docker Compose: uma aplicação web em Flask, um banco PostgreSQL e um cache Redis. A ideia é mostrar como integrar tudo de maneira simples, como faria um estudante curioso que se preocupa com boas práticas básicas.

## Estrutura

```
.
├── docker-compose.yml
├── db
│   └── init.sql
└── web
    ├── .env
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

## Pré-requisitos

- Docker Desktop ou engine compatível com Docker Compose v2

## Como rodar

1. Suba os serviços:

   ```powershell
   docker compose up --build
   ```

2. Acesse a aplicação:

   - Navegador: http://localhost:8000/
   - Healthcheck: http://localhost:8000/health

3. Observe o contador sendo incrementado a cada requisição, provando que a aplicação conversa com o PostgreSQL e usa o Redis como cache.

### Testando a comunicação manualmente

- Banco de dados:

  ```powershell
  docker compose exec db psql -U student -d student_notes -c "SELECT * FROM visit_counter;"
  ```

- Cache:

  ```powershell
  docker compose exec cache redis-cli GET visit_counter:homepage
  ```

- Aplicação:

  ```powershell
  curl http://localhost:8000/
  ```

Esses comandos dão uma visão rápida da comunicação entre os serviços.

## Encerrando

```powershell
docker compose down -v
```

Isso remove containers e volume do banco, garantindo um recomeço limpo.
