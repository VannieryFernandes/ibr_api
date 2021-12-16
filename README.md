## Pré-requisitos para instalação:

1. Criar uma enviroment python da versão 3.7 .
2. Configuração correta no .env integrado ao banco de dados Postgresql 12
3. Criar banco no postgres igual definido no .env

## Baixar e Instalar as bibliotecas

Usamos Pipenv para gerenciar bibliotecas e criar enviroments

```
1. $ git clone https://github.com/VannieryFernandes/ibr_api.git

2. $ cd api_clients

3. $ pipenv install

4. $ pipenv shell (ativar enviroment)

5. $ uvicorn main:app --reload

```
Acessar documentação Swagger no navegador: [http://localhost:8000/docs].


## Arquitetura do projeto

```
│
├── main.py
├── .env.example
├── .gitignore
├── package.json
├── package-lock.json
├── Pipfile
├── Pipfile.lock
├── README.md
└── app ── v1
            ├── Controllers
            │       └── fileController.py     
            ├── Exceptions
            │       └── fileException.py
            ├── Models
            │       └── fileModel.py
            ├── Resources
            │       └── fileResource.py
            ├── Schemas
            │       └── fileSchema.py
            ├── db_postgres.py
            └── routers.py
    

```

