# Desafio 5 - Arquitetura com API Gateway

Este projeto monta uma pequena arquitetura de microsserviços focada em dois domínios: usuários e pedidos. Um API Gateway centraliza o acesso aos dados e expõe endpoints amigáveis.

## Serviços

- **Gateway (`http://localhost:3000`)**: expõe `/users`, `/users/:id`, `/orders` e `/orders/:id`, repassando as requisições para os microsserviços correspondentes.
- **Users Service (`http://localhost:3001`)**: mantém os dados de usuários.
- **Orders Service (`http://localhost:3002`)**: retorna os pedidos e permite filtrar por usuário via `/users/:userId/orders`.

Cada serviço foi construído com Express e segue práticas simples, como tratamento básico de erros e checagens de saúde em `/health`.

## Como executar

1. Certifique-se de ter o Docker e o Docker Compose instalados.
2. Da raiz do projeto, execute:

   ```powershell
docker-compose up --build
   ```

3. Após a subida dos containers, teste os endpoints:
   - `curl http://localhost:3000/users`
   - `curl http://localhost:3000/orders`
   - `curl http://localhost:3000/users/u1`
   - `curl http://localhost:3000/orders/o1`

Para encerrar, use `Ctrl + C` no terminal e, se quiser remover os containers, execute `docker-compose down`.

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

A ideia é simples, mas suficiente para experimentar uma topologia clássica com um gateway orquestrando diferentes serviços.
