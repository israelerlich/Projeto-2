# Microsservicos Flask

## Visão geral da solucao

Aplicacao exemplo que demonstra comunicacao entre dois microsservicos Flask executados em containers Docker. O Servico A publica uma lista estatica de usuarios e o Servico B consome essa informacao para gerar mensagens formatadas. O Docker Compose orquestra ambos os containers em uma rede bridge unica, permitindo que os servicos conversem pelo nome DNS do container.

## Arquitetura e decisoes tecnicas

- **Servico A (`servico-a/app.py`)**: API REST simples que expone `/users`, retornando uma lista fixa de usuarios. O objetivo e simular um provedor de dados.
- **Servico B (`servico-b/app.py`)**: API REST que consulta `servico-a` via HTTP (`requests` + timeout de 5s), transforma os dados em mensagens legiveis e expone `/info`.
- **Docker Compose**: cria uma rede interna padrao onde `servico-b` resolve `servico-a` por DNS. A clausula `depends_on` garante que o container de dados seja iniciado primeiro.
- **Isolamento**: cada microservico possui seu proprio `Dockerfile` e ciclo de build, reforcando a independencia de deploy.

## Fluxo de funcionamento

1. O container `servico-a` sobe com Flask ouvindo em `0.0.0.0:5001` e publica a lista de usuarios.
2. O container `servico-b` inicia em `0.0.0.0:5002`, aguarda o compose e, ao receber requisoes em `/info`, faz um GET para `http://servico-a:5001/users`.
3. A resposta JSON e convertida em frases como `Usuario Ana ativo.` e devolvida para o cliente.
4. Caso `servico-a` esteja indisponivel, a chamada gera timeout em cinco segundos e o Flask retornara um erro 500 (nao ha tratamento dedicado neste exemplo).

## Execucao com Docker (recomendado)

1. Construa e suba os containers:
   ```powershell
   docker compose up --build
   ```
2. Aguarde a mensagem `Running on http://0.0.0.0:500x` em ambos os servicos.
3. Valide `servico-a` diretamente:
   ```powershell
   Invoke-WebRequest http://localhost:5001/users | Select-Object -ExpandProperty Content
   ```
4. Valide `servico-b` (o retorno ja depende do outro servico):
   ```powershell
   Invoke-WebRequest http://localhost:5002/info | Select-Object -ExpandProperty Content
   ```
5. Pare os containers quando terminar:
   ```powershell
   docker compose down
   ```

### Teste rapido com curl (alternativa)

```powershell
curl http://localhost:5001/users
curl http://localhost:5002/info
```

## Execucao local sem Docker

1. Crie um ambiente virtual (opcional, mas recomendado):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install flask requests
   ```
2. Em um terminal, execute o Servico A:
   ```powershell
   cd .\servico-a; python app.py
   ```
3. Em outro terminal, execute o Servico B:
   ```powershell
   cd .\servico-b; python app.py
   ```
4. Acesse os mesmos endpoints `http://localhost:5001/users` e `http://localhost:5002/info` para testar.
5. Finalize com `Ctrl+C` em cada terminal.
