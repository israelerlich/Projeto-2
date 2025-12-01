# Docker Compose Multi-Service Playground

Projeto didático que orquestra três serviços interdependentes com Docker Compose: uma API Flask (`web`), um PostgreSQL (`db`) e um Redis (`cache`). A solução foca em demonstrar integração entre componentes, isolamento por container e como automatizar dependências com uma stack leve.

## Arquitetura e decisões técnicas

- **Topologia**: um único arquivo `docker-compose.yml` define a rede interna padrão (`bridge`), volume persistente para o banco e variáveis de ambiente compartilhadas com a aplicação.
- **API Flask**: concentra a lógica de negócio e expõe endpoints HTTP em `http://localhost:8000`. A aplicação grava o total de visitas na tabela `visit_counter` (PostgreSQL) e usa o Redis como cache de leitura.
- **PostgreSQL**: inicia com `init.sql`, garantindo esquema e dados mínimos. Volume nomeado preserva o estado mesmo após `docker compose down` (sem `-v`).
- **Redis**: atua como cache de chave/valor, reduzindo roundtrips no banco para leituras repetidas. Mantém dados efêmeros, logo não persiste volume.
- **Comunicação**: Flask usa as variáveis `POSTGRES_HOST` e `REDIS_HOST` para alcançar os serviços dentro da rede Compose; credenciais e parâmetros ficam no arquivo `.env` consumido pelo `docker-compose.yml`.

```
        +-------------+        +------------+
HTTP --->  |   Flask     | ---->  | PostgreSQL |
        |   web:app   |        |    db      |
        +-------------+        +------------+
            |                     ^
            v                     |
        +-------------+--------------+
        |  Redis      |
        |  cache      |
        +-------------+
```

## Estrutura do repositório

```
.
├── docker-compose.yml    # Orquestra os serviços e rede
├── db
│   └── init.sql          # Criação da tabela visit_counter
└── web
   ├── .env              # Configurações de acesso aos serviços (não versionar em produção)
   ├── Dockerfile        # Build da imagem Flask
   ├── app.py            # Aplicação principal
   └── requirements.txt  # Dependências Python
```

## Como funciona (passo a passo)

- **Subida**: `docker compose up` constrói a imagem `web`, cria containers e conecta cada um na rede padrão.
- **Inicialização**: o container `db` executa `init.sql`, criando a tabela `visit_counter`; `web` aguarda o banco responder antes de aceitar requisições.
- **Fluxo de requisição**: ao acessar `/`, a API verifica o cache Redis; se não houver dado, consulta o PostgreSQL, incrementa o contador e propaga o valor para o Redis.
- **Health check**: endpoint `/health` retorna `200` quando Flask consegue se comunicar com os serviços dependentes.

## Execução passo a passo

1. **Instale os pré-requisitos**
  - Docker Desktop (ou Docker Engine com Compose v2)

2. **Construa e suba os containers**
  ```powershell
  docker compose up --build
  ```

3. **Verifique a aplicação**
  - Navegador: `http://localhost:8000/`
  - Health check: `http://localhost:8000/health`

4. **Teste a comunicação entre serviços**
  - Consultar o contador direto no PostgreSQL:
    ```powershell
    docker compose exec db psql -U student -d student_notes -c "SELECT * FROM visit_counter;"
    ```
  - Conferir o valor em cache no Redis:
    ```powershell
    docker compose exec cache redis-cli GET visit_counter:homepage
    ```
  - Requisitar a API via linha de comando:
    ```powershell
    curl http://localhost:8000/
    ```

5. **Encerrar e limpar**
  ```powershell
  docker compose down -v
  ```
  Remove containers e o volume do banco para um recomeço limpo.
