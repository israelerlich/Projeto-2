# Desafio 5 - Arquitetura com API Gateway

Este desafio apresenta uma topologia de microsserviços dividida em dois domínios principais (usuários e pedidos) orquestrados por um API Gateway. Ele serve como laboratório para explorar padrões de comunicação, desacoplamento entre serviços e isolamento de responsabilidades.

## Arquitetura e decisões técnicas

- **Estilo arquitetural**: microsserviços independentes que comunicam via HTTP, cada um encapsulando seu contexto (users e orders).
- **API Gateway**: camada frontal construída com Express para consolidar chamadas, aplicar roteamento e oferecer um ponto único de entrada (`http://localhost:3000`). Essa abordagem permite evoluir regras de autenticação, caching e observabilidade sem replicar lógica em cada serviço.
- **Dados em memória**: os serviços de domínio utilizam repositórios em memória (arquivos `.js` em `src/data`) para simplificar o cenário. A estrutura foi preparada para troca futura por um banco externo.
- **Comunicação síncrona**: gateway chama os serviços via HTTP usando endereços internos (`users-service:3001`, `orders-service:3002`) definidos pela rede padrão do Docker Compose.
- **Observabilidade básica**: cada serviço expõe `/health` para checagens de disponibilidade e logs estruturados via `console.log` centralizando eventos relevantes.

## Funcionamento dos componentes

- **Containers**: o `docker-compose.yml` cria três containers a partir de imagens Node.js configuradas pelos respectivos `Dockerfile`. Cada container instala dependências e expõe portas distintas (3000, 3001, 3002).
- **Rede**: o Compose gera uma rede bridge nomeada, permitindo que os containers se descubram por hostname (ex.: o gateway acessa `http://users-service:3001/users`). Não há exposição direta dos serviços de domínio para o host, apenas o gateway fica acessível externamente.
- **Fluxo de requisições**:
   - Chamadas chegam ao gateway que identifica a rota desejada.
   - O gateway encaminha a chamada para o serviço correspondente usando `axios`.
   - Os serviços consultam seus repositórios em memória, aplicam filtros (por ID ou por usuário) e retornam ao gateway.
   - O gateway responde para o consumidor, encapsulando eventuais erros (por exemplo, falhas de rede ou registros não encontrados) com mensagens padronizadas.
- **Microsserviços**:
   - `users-service`: expõe `/users`, `/users/:id` e `/health`, mantém o catálogo de usuários em `src/data/users.js` e aplica busca por ID no repositório (`src/repositories/userRepository.js`).
   - `orders-service`: expõe `/orders`, `/orders/:id`, `/users/:userId/orders` e `/health`, consumindo dados de `src/data/orders.js`. Implementa lógica de filtragem por usuário em `src/services/orderService.js`.

## Passo a passo de execução

### Pré-requisitos

- Docker Desktop ou Docker Engine 20+ com Docker Compose habilitado.
- Porta 3000 livre no host (o gateway a utiliza). As portas 3001 e 3002 ficam isoladas na rede interna.

### Subindo os containers

1. Abra um terminal PowerShell na raiz do projeto (`desafio5`).
2. Construa e inicialize todo o stack:

    ```powershell
docker-compose up --build
    ```

    - O Compose cria a rede, monta cada container, instala dependências (`npm install`) e inicia os servidores Express.
    - Aguarde as mensagens de log indicando que os serviços estão ouvindo nas portas configuradas.

3. (Opcional) Utilize outro terminal para conferir o status:

    ```powershell
docker ps --filter "name=desafio5"
    ```

### Testando a solução

- Valide a saúde dos serviços:

   ```powershell
curl http://localhost:3000/health
   ```

- Liste recursos expostos pelo gateway:

   ```powershell
curl http://localhost:3000/users
curl http://localhost:3000/orders
   ```

- Consulte registros específicos e fluxos compostos:

   ```powershell
curl http://localhost:3000/users/u1
curl http://localhost:3000/orders/o1
curl http://localhost:3000/users/u1/orders
   ```

### Encerrando e limpeza

- Interrompa os containers ativos com `Ctrl + C` no terminal que roda o Compose.
- Remova containers, redes e imagens intermediárias criadas para o desafio:

   ```powershell
docker-compose down --rmi local --volumes
   ```

## Estrutura de pastas

```
.
├── docker-compose.yml
├── gateway
│   ├── Dockerfile
│   ├── package.json
│   └── src
├── orders-service
│   ├── Dockerfile
│   ├── package.json
│   └── src
└── users-service
      ├── Dockerfile
      ├── package.json
      └── src
```

Essa organização realça a independência de cada microsserviço, facilita a evolução isolada de funcionalidades e mantém o gateway como fachada controladora do ecossistema.
