# Neo4j Blog

Aplicação exemplo para a criação de um blog em Python utilizando Flask e Neo4J

## Iniciando

// TO-DO

### Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:
* [Git](https://git-scm.com)
* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação (Desenvolvimento Local)

```bash
# Clone este repositório
$ git clone https://github.com/rahenrique/neo4jblog.git

# Execute a aplicação em modo de desenvolvimento, utilizando o servidor embarcado
$ docker-compose up -d
```

```bash
# Opcionalmente, é possível executar a aplicação utilizando Gunicorn
# Basta forçar o uso do arquivo docker-compose.yml sem overrides
$ docker-compose -f docker-compose.yml up -d
```

O servidor Flask inciará na porta:5000 em modo de desenvolvimento. Qualquer alteração de código-fonte irá refletir automaticamente na aplicação em execução.

Caso seja a primeira vez que a aplicação é iniciada, será necessário criar as tabelas do banco de dados da aplicação:
```bash
$ docker exec -it flask flask init-db
```

App: <http://0.0.0.0:5000/>
Neo4jBrowser: <http://localhost:7474/browser/>

## Executando testes

// TO-DO

## Deployment

// TO-DO

## Built With

* [Flask](https://flask.palletsprojects.com/)
* [Neo4j](https://neo4j.com/)
* [nginx](https://nginx.org/en/)