# Microsserviços com Flask e Docker

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

Este projeto é uma prova de conceito que demonstra a comunicação e orquestração entre dois microsserviços **Flask** rodando em containers.

O objetivo principal é exemplificar como serviços distintos podem trocar informações dentro de uma rede segura gerenciada pelo Docker Compose, utilizando resolução de nomes via DNS interno.

## 🏗 Arquitetura e Decisões Técnicas 

[Image of microservices communication diagram]


A solução adota o padrão de arquitetura distribuída onde cada serviço possui uma responsabilidade única:

* **Serviço A (Provider):**
    * Atua como a fonte da verdade (Data Provider).
    * Expõe uma API REST simples que fornece uma lista estática de usuários.
* **Serviço B (Consumer):**
    * Atua como agregador/cliente.
    * Consome os dados do *Serviço A* via HTTP (utilizando a biblioteca `requests` com timeout de segurança).
    * Processa e formata as informações antes de entregar ao cliente final.
* **Docker Compose (Orquestrador):**
    * Cria uma rede `bridge` dedicada.
    * Permite que o *Serviço B* encontre o *Serviço A* simplesmente chamando pelo nome do container (`http://servico-a:5001`), sem necessidade de configurar IPs fixos.

## 🧩 Componentes do Sistema

| Serviço | Porta (Host) | Endpoint Principal | Função |
| :--- | :---: | :--- | :--- |
| **Serviço A** | `5001` | `/users` | Retorna JSON com lista bruta de usuários. |
| **Serviço B** | `5002` | `/info` | Consome o Serviço A e retorna frases formatadas. |

### Fluxo de Funcionamento
1.  O **Serviço A** inicia e fica escutando na porta 5001.
2.  O **Serviço B** inicia, aguarda requisições e, quando acionado em `/info`, dispara um GET interno para o Serviço A.
3.  Se o Serviço A estiver online, os dados são processados e retornados.
4.  Se o Serviço A estiver offline, o Serviço B gera um erro (timeout de 5s).

## 🚀 Execução com Docker (Recomendado)

Esta é a forma mais simples de rodar, pois garante que a rede e as dependências estejam isoladas.

### 1. Subir a aplicação
No terminal, execute o comando abaixo para construir as imagens e iniciar os containers:

```bash
docker compose up --build
```

2. Testar os Endpoints
Com os containers rodando, você pode testar via navegador ou terminal:
```bash
# Teste direto no Provedor de Dados (Serviço A)
curl http://localhost:5001/users

# Teste no Consumidor (Serviço B) - Este aciona o Serviço A internamente
curl http://localhost:5002/info
```

3. Encerrar
Para parar e remover os containers:
```bash
docker compose down
```

⚙️ Execução Local (Sem Docker)
Caso queira rodar diretamente no Python em sua máquina (para desenvolvimento ou debug), siga os passos:

Configurar Ambiente Virtual:
```bash
python -m venv .venv
# No Windows:
.\.venv\Scripts\Activate.ps1
# No Linux/Mac:
source .venv/bin/activate

pip install flask requests
```

Rodar o Serviço A: Abra um terminal e execute:
```bash
cd servico-a
python app.py
```

Rodar o Serviço B: Abra um segundo terminal e execute:
```bash
cd servico-b
python app.py
```


