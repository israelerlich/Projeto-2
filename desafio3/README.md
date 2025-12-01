# Docker Compose Playground: Flask, Postgres & Redis

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Este projeto é um laboratório prático de orquestração de containers. Ele demonstra a integração entre uma aplicação **Python (Flask)**, um banco de dados relacional (**PostgreSQL**) e um sistema de cache em memória (**Redis**).

O objetivo é exemplificar padrões de arquitetura como persistência de dados, *caching* para performance e isolamento de dependências usando uma stack leve e automatizada.

## 🏗 Arquitetura e Decisões Técnicas


A infraestrutura é definida inteiramente via código (`IaC`) no `docker-compose.yml`, criando um ambiente isolado onde:

* **API Flask (`web`)**: Centraliza a regra de negócio. Implementa o padrão **Cache-Aside**: tenta ler do Redis primeiro; se falhar, busca no Postgres e atualiza o cache.
* **PostgreSQL (`db`)**: Armazena o estado persistente (contador de visitas). Utiliza um *Volume Docker* para garantir que os dados sobrevivam ao reinício dos containers.
* **Redis (`cache`)**: Atua como armazenamento efêmero de chave/valor para reduzir a carga no banco de dados e acelerar a resposta de leitura.
* **Networking**: Todos os serviços comunicam-se através de uma rede `bridge` interna, utilizando os nomes dos serviços (`db`, `cache`) como *hostnames*.

### Fluxo de Dados Simplificado

```mermaid
graph LR
    User(Cliente HTTP) --> API[Flask API :8000]
    API -- 1. Verifica Cache --> Redis[(Redis)]
    API -- 2. Se falhar, lê/grava --> DB[(PostgreSQL)]
    DB -- 3. Retorna dado --> API
    API -- 4. Atualiza Cache --> Redis
```

🚀 Como Executar
Pré-requisitos
- Docker Desktop ou Docker Engine instalado.
  1. Inicializar o Ambiente
O comando abaixo constrói a imagem da aplicação, baixa as imagens do Postgres e Redis, e inicia toda a stack.
```bash
docker compose up --build
```

2. Verificar Funcionamento
Acesse o navegador ou use o curl para interagir com a API:

Página Principal: http://localhost:8000/
Health Check: http://localhost:8000/health

```bash
# Teste via terminal
curl http://localhost:8000/
```

3. Inspecionar os Serviços (Debug)
Você pode executar comandos diretamente dentro dos containers em execução para validar se os dados estão sendo gravados corretamente.

Consultar o Banco de Dados (PostgreSQL):
```bash
docker compose exec db psql -U student -d student_notes -c "SELECT * FROM visit_counter;"
```

Consultar o Cache (Redis):
```bash
docker compose exec cache redis-cli GET visit_counter:homepage
```

4. Encerrar e Limpar
Para parar os serviços e remover os volumes (resetar o banco de dados):
```bash
docker compose down -v
```





