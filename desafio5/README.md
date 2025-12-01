# Desafio 5: Arquitetura de Microsserviços com API Gateway

![NodeJS](https://img.shields.io/badge/Node.js-20-43853D?style=for-the-badge&logo=node.js&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Express](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)

Este projeto implementa uma arquitetura de microsserviços dividida em dois domínios de negócio (**Users** e **Orders**), orquestrados por um **API Gateway**.

O objetivo é servir como um laboratório prático para explorar padrões de comunicação distribuída, desacoplamento de serviços e centralização de requisições.

## 🏗 Arquitetura e Decisões Técnicas

A solução foi desenhada priorizando a simplicidade da infraestrutura para focar nos padrões de arquitetura:

* **API Gateway (BFF - Backend for Frontend):**
    * Construído com **Express**.
    * Atua como ponto único de entrada (`http://localhost:3000`).
    * Centraliza o roteamento e simplifica o consumo por parte do cliente, evitando que o front-end precise conhecer os endereços de cada microsserviço.
* **Microsserviços Desacoplados:**
    * Cada serviço (`users-service` e `orders-service`) possui seu próprio contexto delimitado.
    * Comunicação **síncrona via HTTP** utilizando a rede interna do Docker.
* **Persistência In-Memory:**
    * Para fins didáticos, os dados são persistidos em memória (arquivos `.js` e vetores), eliminando a complexidade de configurar bancos de dados externos neste estágio.
* **Observabilidade Básica:**
    * Implementação de *Health Checks* em todos os serviços.
    * Logs estruturados no console para rastreamento de requisições.

## 🧩 Componentes do Sistema

| Componente | Porta Externa | Porta Interna | Descrição |
| :--- | :---: | :---: | :--- |
| **API Gateway** | `3000` | `3000` | Recebe as requisições externas e as encaminha para os serviços internos via rede `bridge`. |
| **Users Service** | - | `3001` | Gerencia o catálogo de usuários. Acessível apenas pelo Gateway. |
| **Orders Service** | - | `3002` | Gerencia os pedidos e consome dados de usuários quando necessário. |

### Fluxo de Requisição
1.  O cliente chama o Gateway (`GET /users/u1`).
2.  O Gateway identifica a rota e dispara uma requisição HTTP interna (`axios`) para `http://users-service:3001/users/u1`.
3.  O serviço processa a lógica de domínio e retorna o JSON.
4.  O Gateway padroniza a resposta e a devolve ao cliente.

## 🚀 Como Executar

### Pré-requisitos
* [Docker](https://www.docker.com/) e Docker Compose instalados.
* Porta `3000` livre no seu computador.

### Passo a Passo

1.  **Clone o repositório e acesse a pasta:**
    ```bash
    git clone <seu-repo>
    cd desafio5
    ```

2.  **Suba o ambiente com Docker Compose:**
    Este comando irá construir as imagens, criar a rede isolada e iniciar os containers.
    ```bash
    docker-compose up --build
    ```

3.  **Verifique se está tudo rodando:**
    ```bash
    docker ps --filter "name=desafio5"
    ```

## 📡 Endpoints Disponíveis

Você pode testar a API utilizando `curl`, Postman ou o navegador.

| Método | Rota (Gateway) | Descrição |
| :--- | :--- | :--- |
| `GET` | `/health` | Verifica a saúde do Gateway e conectividade básica. |
| `GET` | `/users` | Lista todos os usuários cadastrados. |
| `GET` | `/users/:id` | Busca detalhes de um usuário específico (ex: `u1`). |
| `GET` | `/orders` | Lista todos os pedidos. |
| `GET` | `/orders/:id` | Busca detalhes de um pedido específico. |
| `GET` | `/users/:id/orders` | **Aggregator Pattern**: Busca todos os pedidos de um usuário específico. |

**Exemplos de teste no Terminal:**

```bash
# Verificar saúde do sistema
curl http://localhost:3000/health

# Listar usuários
curl http://localhost:3000/users

# Buscar pedidos do usuário 'u1'
curl http://localhost:3000/users/u1/orders
