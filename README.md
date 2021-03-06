# Cadastro de Contas a Pagar

Cadastro de contas a pagar é um microsserviço para manter contas.

É possível cadastrar, atualizar, remover, buscar e listar as contas cadastradas.

A API foi construída com [FastApi](https://fastapi.tiangolo.com/).

## Prerequisites

Caso o desenvolvedor opte por executar a solução de forma não _dockerizada_, sugere-se a criação de um ambiente virtual para instalação das dependências da aplicação, como por exemplo o [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

Para instalar as dependências do projeto, execute:

```bash
pip3 install -e .
```

Além disso, é preciso inicializar os softwares de dependência, são eles:

* [`PostgreSQL`](https://www.postgresql.org): Banco de dados relacional para manter uma conta a pagar.
* [`PGAdmin`](https://www.pgadmin.org): Permite a comunicação com o banco de dados `PostgreSQL` através de uma interface gráfica, exposta por uma URL.

No cenário em que o desevolvedor opte por executar a aplicação de forma _dockerizada_ (recomendada) é preciso possuir o [docker](https://docs.docker.com/) e o [docker-compose](https://docs.docker.com/compose/) instalados.

As variáveis de ambiente consumidas pela aplicação encontram-se _setadas_ no arquivo [cadastro_contas.yml](cadastro_contas.yml), assim, não é preciso que o desenvolvedor as configure, são eles:

* `PGADMIN_DEFAULT_EMAIL`: _email_ utilizado no momento de criação do container `PGAdim` permitindo o login;
* `PGADMIN_DEFAULT_PASSWORD`: _password_ utilizado no momento de execução do container `PGAdim` permitindo o login;

* `POSTGRES_DB`: Nome do banco de dados utilizado para criação do banco de dados, consumido pelo container do banco de dados;
* `POSTGRES_USER`: Usuário do banco de dados utilizado para criação do banco de dados, consumido pelo container do banco de dados;
* `POSTGRES_PASSWORD`: Senha do banco de dados utilizado para criação do banco de dados, consumido pelo container do banco de dados.

### Instalação e Execução

A execução da aplicação é dividida em duas partes: `build` das imagens consumidas pelos containers e a execução dos containers. Para o [build](./build.sh) das imagens é necessário executar o seguinte comando:

```bash
bash build.sh
```

Com as imagens _buildadas_ é possível executar os containers, através do comando:

```bash
bash run.sh
```

Com a aplicação no ar, basta acessar o [ReDoc](http://localhost:5000/v1/docs) para saber como utilizar cada um dos *endpoints* e para utilizar os *endpoints* acesse o [Swagger](http://localhost:5000/v1/swagger).

Com todo o ambiente rodando, antes mesmo de instalar e rodar a aplicação, é preciso executar a query de criação no banco de dados. Entre no PGAdmin configure o acesso ao banco de dados e execute a query do arquivo [`create.sql`](./cadastro_contas/scripts/create.sql).

## Executando testes

Os testes da aplicação realizam a validação das respostas às requisições dos endpoints, validando o código de retorno esperado, o conteúdo do retorno e o tipo do retorno.

O ideal é que os testes sejam executados de forma _dockerizada_, para tanto,  é preciso que os _containers_ da API e do banco de dados estejam em execução, o que pode ser feito seguindo as instruções em `Instalação e Execução`.

Com o container da API nomeado como `cadastro`, execute:

```bash
docker container exec -it cadastro pytest -v
```

### Estilo de código

Esse código segue o padrão PEP8 e pode ser testado com a biblioteca [PyLama](https://github.com/klen/pylama) como no exemplo a seguir

```bash
pip3 install pylama
pylama -o pylama.ini .
```

## Deploy

Com a aplicação _dockerizada_ e testada, é possível efetuar o _deploy_ em um orquestrador de _containers_ a exemplo do [Kubernetes](https://kubernetes.io/pt/), ou mesmo, com o orquestrador nativo do Docker - [Swarm](https://docs.docker.com/engine/swarm/).

## Construído Com

* [loguru](https://github.com/Delgan/loguru)
* [pydantic](https://pydantic-docs.helpmanual.io)
* [fastapi](https://fastapi.tiangolo.com)
* [uvicorn](https://www.uvicorn.org)
* [gunicorn](https://gunicorn.org)
* [sphinx](https://www.sphinx-doc.org/en/master/)
* [uvloop](uvloop)

## Versionamento

O versionamento segue o padrão do [Versionamento Semântico](http://semver.org/). Para saber as versões de repositório entre nas [tags](https://github.com/kevinsantana/desafio-tecnico-deliver-it/tags).

## License

Todos os direitos são reservados ao autor Kevin de Santana Araujo.

## Outras informações

* Caso tenha alguma dúvida em relação ao projeto, ou queira contribuir com sugestões ou críticas, abra uma `issue` ou procure o desenvolvedor através do email kevin_santana.araujo@hotmail.com
