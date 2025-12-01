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
