# Microsservicos Flask

Este projeto utiliza dois microsservicos independentes escritos em Flask:

- **Servico A** (`servico-a/app.py`): expone `/users` com uma lista fixa de usuarios.
- **Servico B** (`servico-b/app.py`): consome o Servico A e gera mensagens prontas em `/info`.

## Requisitos

- Python 3.10+
- Docker 24+

## Execucao com Docker (recomendado)

1. Construa e suba os containers:
   ```powershell
   docker compose up --build
   ```
2. Teste os endpoints com o navegador ou `Invoke-WebRequest`:
   - `http://localhost:5001/users`
   - `http://localhost:5002/info`

## Execucao local sem Docker

1. Abra dois terminais na raiz do projeto.
2. No primeiro terminal, execute o Servico A:
   ```powershell
   cd .\servico-a; python app.py
   ```
3. No segundo terminal, execute o Servico B:
   ```powershell
   cd .\servico-b; python app.py
   ```
4. Acesse os endpoints nas mesmas URLs utilizadas para o Docker.

## Estrutura de pastas

```
/ servico-a
  \_ app.py
  \_ Dockerfile
/ servico-b
  \_ app.py
  \_ Dockerfile
docker-compose.yml
```
