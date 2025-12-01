# Desafio Docker: Comunicação entre Containers

Projeto demonstrativo criado para o desafio da disciplina, mostrando como dois containers Docker conseguem conversar entre si usando uma rede bridge customizada.

## 🧭 Visão Geral da Solução

- **Arquitetura enxuta**: Dois microsserviços isolados (servidor Flask e cliente Alpine) conectados pela mesma rede Docker bridge.
- **Automação via PowerShell**: Scripts `run_challenge.ps1` e `cleanup.ps1` cuidam do ciclo completo (setup → testes → teardown) para evitar comandos manuais e garantir repetibilidade.
- **Decisões técnicas**:
  - Python Flask escolhido pela simplicidade para expor um endpoint HTTP e logar as requisições.
  - Alpine como cliente para manter a imagem leve; o `curl` é instalado somente em runtime.
  - Rede nomeada (`minha-rede-customizada`) para permitir resolução de nomes (`container-servidor`) sem depender de IP fixo.

## 🏗️ Como a Arquitetura Funciona

- **server/app.py**: Flask responde na porta 8080 com a mensagem “Olá do Servidor!” e registra a origem da requisição.
- **server/Dockerfile**: Base `python:3.9-slim`, copia `app.py`, instala Flask e expõe a porta 8080.
- **run_challenge.ps1**:
  1. Limpa containers/rede antigos (idempotência).
  2. Cria rede bridge `minha-rede-customizada`.
  3. Faz o build da imagem `meu-servidor-web` usando o `Dockerfile` do servidor.
  4. Sobe `container-servidor` (publica porta 8080 no host).
  5. Sobe `container-cliente`, que roda um loop `curl` a cada 5s.
  6. Exibe os últimos logs de ambos para comprovar a troca de mensagens.
- **Fluxo de comunicação**: o cliente resolve o hostname `container-servidor` via DNS da rede Docker, envia `GET /`, recebe HTTP 200 com timestamp, e o servidor registra o IP de origem no log.
- **cleanup.ps1**: derruba os containers e remove a rede, garantindo que o ambiente volte ao estado inicial para outro teste.

Estrutura dos arquivos:

```
.
├── server/
│   ├── app.py
│   └── Dockerfile
├── run_challenge.ps1
├── cleanup.ps1
└── README.md
```

## ▶️ Execução Passo a Passo

### Pré-requisitos
- Docker Desktop instalado e em execução.
- PowerShell (Windows PowerShell 5.1 ou PowerShell 7+).

### 1. Subir o ambiente e validar comunicação
```powershell
powershell -File run_challenge.ps1
```
O script mostrará:
- Rede criada (`docker network create` sucesso).
- ID dos containers gerados.
- Logs finais exibindo respostas 200 com a mensagem “Olá do Servidor!”.

### 2. (Opcional) Inspecionar recursos manualmente
```powershell
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker network inspect minha-rede-customizada
Invoke-WebRequest http://localhost:8080 | Select-Object -ExpandProperty Content
```
Esses comandos rendem prints úteis: tabelas de containers ativos, detalhes da rede e resposta direta do servidor.

### 3. Limpar o ambiente
```powershell
powershell -File cleanup.ps1
```
Remove containers e rede para que novos testes comecem limpos.


## 🛠️ Detalhes Técnicos Extras

- Servidor exposto em `localhost:8080` com mapeamento de porta (`-p 8080:8080`).
- Loop do cliente roda em shell Alpine (`/bin/sh -c`), com pausa de 5 segundos para simular um polling simples.
- `Set-StrictMode` e tratamento de erros nos scripts PowerShell ajudam a evitar estados inconsistentes caso o Docker esteja desligado ou os recursos não existam mais.

## Autores

- [@GuitGud](https://github.com/GuitGud)
- [@israelerlich](https://github.com/israelerlich)
