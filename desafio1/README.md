# Desafio Docker: Comunicação e Automação com PowerShell

![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PowerShell](https://img.shields.io/badge/PowerShell-5391FE?style=for-the-badge&logo=powershell&logoColor=white)

Este projeto demonstra a comunicação entre containers isolados utilizando uma **rede Bridge customizada**.

Além da infraestrutura Docker, o projeto foca em **automação**: todo o ciclo de vida (criação da rede, build, execução e limpeza) é gerenciado por scripts PowerShell, garantindo que o ambiente de teste seja reprodutível e livre de erros manuais.

## 🏗 Arquitetura e Decisões Técnicas

A solução é composta por dois microsserviços leves que conversam entre si via DNS interno do Docker:

* **Servidor (`server`)**: Uma aplicação **Flask** minimalista que expõe a porta `8080` e loga o IP de quem fez a requisição.
* **Cliente (`client`)**: Um container **Alpine Linux** (ultra-leve) que executa um loop de requisições `curl` a cada 5 segundos.
* **Rede Customizada**: Utilizamos uma rede nomeada (`minha-rede-customizada`) em vez da bridge padrão. Isso permite a **Resolução de DNS Automática**, onde o cliente acessa o servidor pelo nome `container-servidor`, sem precisar saber o IP.

### Fluxo de Comunicação

```mermaid
graph LR
    Client[Container: Cliente (Alpine)] -- "curl http://container-servidor:8080" --> Net((Rede Docker Bridge))
    Net -- "Resolve DNS & Encaminha" --> Server[Container: Servidor (Flask)]
    Server -- "HTTP 200 OK" --> Client
```

🧩 Componentes do Projeto:
Arquivo/Container,Tipo,Função
server/app.py,App,Responde na porta 8080 e registra logs de acesso.
run_challenge.ps1,Script,"Setup: Limpa resíduos, cria rede, builda imagem e sobe containers."
cleanup.ps1,Script,Teardown: Para e remove containers e a rede criada.
container-cliente,Container,Simula um usuário fazendo polling contínuo no servidor.

🚀 Execução Passo a Passo
Pré-requisitos
Docker Desktop instalado e rodando.

PowerShell 5.1 ou superior (Windows) ou PowerShell Core (Linux/Mac).

1. Automação: Subir o Ambiente
Execute o script principal. Ele fará todo o trabalho pesado (limpeza preventiva, build e run).


```bash
powershell -File run_challenge.ps1
```

O que acontece?

Mensagem de criação da rede com sucesso.

Logs em tempo real mostrando o cliente recebendo "Olá do Servidor!".

2. Validação Manual
Se quiser inspecionar o ambiente enquanto ele roda:

```bash
# Ver tabela de containers e portas
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Inspecionar detalhes da rede bridge
docker network inspect minha-rede-customizada

# Testar o servidor diretamente do seu host
Invoke-WebRequest http://localhost:8080 | Select-Object -ExpandProperty Content
```

3. Limpeza do Ambiente
Para garantir que não sobrem containers "órfãos" consumindo recursos, execute o script de limpeza:

```bash
powershell -File cleanup.ps1
```

