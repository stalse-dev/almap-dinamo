
# DataHub Base 


Serviço base do DataHub



## Instalação

Instale my-project com npm

```bash
  npm install my-project
  cd my-project
```
    
## Rodando localmente

Clone o projeto

```bash
git clone git@github.com:stalse-dev/datahub_base.git
```

Entre no diretório do projeto

```bash
cd datahub_base
```

Crie e ative um ambiente virtual 

```bash
python -m venv .venv
.venv\Scripts\Activate
```

Instale as dependências

```bash
pip install -r requirements.txt
```

Aplique a migrações

```bash
python manage.py migrate
```

Inicie o servidor

```bash
python manage.py runserver
```

## Variáveis de Ambiente

Para rodar esse projeto, você vai precisar adicionar as seguintes variáveis de ambiente no seu .env

`SECRET_KEY`
`DB_NAME`
`DB_USER`
`DB_PASSWORD`
`DB_PUBLIC_IP`
`DB_INSTANCE`

`GOOGLE_PROJECT_ID`
`GOOGLE_APPLICATION_CREDENTIALS`
`ON_GOOGLE_CLOUD`

`MANAGE_PY_PATH`