# Demonstracao de Persistencia com Volumes Docker

Este projeto demonstra, de ponta a ponta, como persistir dados fora do ciclo de vida de containers usando Docker Compose, um volume nomeado e um banco SQLite simples. Dois microsservicos Python compartilham o mesmo volume: um escreve dados (writer) e outro le os dados (reader), comprovando que o estado sobrevive apos a remocao dos containers.

## Pre-requisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e em execucao.
- PowerShell 5.1 ou superior (padrao nas instalacoes modernas do Windows).

## Descricao da solucao e decisoes tecnicas
- **Linguagem**: Python 3.12 sobre imagem `python:3.12-alpine` para manter a imagem leve e com bibliotecas necessarias para SQLite.
- **Banco**: SQLite foi escolhido por ser embutido, nao exigir servico dedicado e permitir demonstrar volumes com apenas um arquivo (`demo.db`).
- **Persistencia**: volume nomeado `sqlite_data` montado em `/data` para ambos os containers. Como o volume fica fora do filesystem efemero do container, o arquivo do banco sobrevive a recriacoes.
- **Orquestracao**: `docker-compose.yml` organiza os serviços, build compartilhado e montagem do volume. Mantem a topologia simples, ideal para laboratoriar.
- **Scripts**: `write_data.py` prepara o banco e carrega registros iniciais; `read_data.py` valida a leitura do mesmo arquivo. Os scripts incluem docstrings e uso de context manager para boas praticas.

## Arquitetura e funcionamento detalhado
- **Servicos**: 
  - `writer`: container responsavel por garantir a existencia da tabela `customers` e inserir registros exemplo (Alice, Bruno, Carla).
  - `reader`: container que acessa o mesmo volume, abre o arquivo `demo.db` e lista os clientes persistidos.
- **Volume**: `sqlite_data` eh criado automaticamente pelo Compose. Mesmo apos o `writer` ser destruido (`--rm`), o arquivo fica armazenado no volume e pode ser montado por qualquer outro container.
- **Rede**: Compose cria a rede `desafio2_default`. Os containers nao dependem de comunicacao via TCP entre si, mas a rede permite extensao facil (por exemplo, adicionar um dashboard Flask).
- **Fluxo**: 
  1. Build da imagem compartilhada (contendo os dois scripts).
  2. Execucao do `writer`, que popula o banco e encerra.
  3. Execucao posterior do `reader`, que confirma a existencia dos dados.
  4. Opcionalmente, inspecao manual do volume para visualizar o arquivo `demo.db`.

## Estrutura do repositorio
- `Dockerfile`: constroi a imagem base Python com o diretório `app` copiado para `/app`.
- `docker-compose.yml`: define servicos, comandos e volume nomeado.
- `app/write_data.py`: cria ou atualiza `demo.db` com registros padrao.
- `app/read_data.py`: lista os registros persistidos.
- `README.md`: documentacao para reproducao do experimento.

## Passo a passo detalhado
Execute os comandos no diretorio raiz do projeto (`desafio 2`).

1. **Construir a imagem compartilhada**
   ```powershell
   docker compose build
   ```
   - Gera uma unica imagem base usada pelos serviços `writer` e `reader`.

2. **Popular o volume com o writer**
   ```powershell
   docker compose run --rm writer
   ```
   - Cria a tabela `customers` se necessario.
   - Insere registros padrao utilizando `INSERT OR IGNORE` para evitar duplicacao em rodadas futuras.
   - Encerra o container (removido por causa do `--rm`), mas o volume permanece com `demo.db`.

3. **Validar a persistencia com o reader**
   ```powershell
   docker compose run --rm reader
   ```
   - Monta o mesmo volume `sqlite_data`.
   - Abre `demo.db` e lista os clientes, comprovando que o arquivo sobreviveu ao desligamento do writer.

4. **(Opcional) Inspecionar o volume manualmente**
   ```powershell
   docker volume ls
   docker run --rm -v desafio2_sqlite_data:/data alpine ls -R /data
   ```
   - O nome real do volume segue o padrao `<pasta>_sqlite_data`; ajuste o comando conforme necessario.

5. **Limpar ambiente**
   ```powershell
   docker compose down
   docker volume rm desafio2_sqlite_data  # remova apenas se quiser apagar o banco
   ```
   - O primeiro comando remove containers e rede. O segundo apaga o volume, eliminando os dados.

## Possiveis extensoes
- Substituir SQLite por PostgreSQL montando o volume em `/var/lib/postgresql/data`.
- Adicionar um terceiro servico (por exemplo, API Flask) que consuma o mesmo banco.
- Automatizar testes para garantir que o volume seja recriado corretamente em pipelines CI.
