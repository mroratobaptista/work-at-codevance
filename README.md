# Work At Codevance

Este projeto tem por finalidade demonstrar todas as habilidades técnícas solicitadas no README-CODEVANCE.md

## Requisitos

- Python 3.9
- Pipenv
- Redis

### Clonar repositório

```shell
git clone https://github.com/mroratobaptista/work-at-codevance.git
```

### Acessar pasta do projeto

```shell
cd work-at-codevance
```

### Copiar arquivo .env-sample

```shell
cp contrib/.env-sample .
```

### Renomear arquivo para .env

```shell
mv .env-sample .env
```

### Instalar todas as libs necessárias, inclusive as de desenvolvimento

```shell
pipenv sync -d
```

### Ativar shell do projeto

```shell
pipenv shell
```

### Coletar arquivos estáticos

```shell
python manage.py collectstatic
```

### Criar banco de dados

```shell
python manage.py migrate
```

### Criar usuário Admin

```shell
python manage.py createsuperuser
```

### Rodar Servidor

```shell
python manage.py runserver
```

### Ativar Worker (Celery)

**Abra outra aba ou terminal e execute**

### Ativar shell do projeto

```shell
pipenv shell
```

### Ativar Worker Celery

```shell
celery -A work_at_codevance worker
```

## Configuração Inicial

1. Acesse [Django Admin](http:127.0.0.1:8000/admin).
2. Crie 2 grupos.
    1. Operador
    2. Fornecedor
3. Inclua o grupo Operador no usuário Admin criado anteriormente e/ou em outro usuário que gostaria.
4. Crie os usuários dos fornecedores e adicione o grupo Fornecedor em cada um deles.
5. Crie os fornecedores e selecione seus respectivos usuários.
6. Crie os pagamentos e selecione seus respectivos fornecedores.

## Documentação API

A API tem 2 endpoints, além dos tradicionais **/api/token/** e **/api/token/refresh/** do Django Rest Framework.

- /api/pagamentos/
- /api/solicitar-adiantamento/

Primeiramente é necessário pegar o token para ter acesso a API através do endpoint **/api/token/**.

### /api/token/

Retorna access_token e refresh_token

Requisição

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"email": "email@email.com", "password": "password"}' \
  http://localhost:8000/api/token/
```

Resposta

```json
{
  "refresh": "refresh_token",
  "access": "access_token"
}
```

---

### /pagamentos/

Retona todos os pagamentos do usuário.

Requisição

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/
```

Resposta

```json
{
  "count": 5,
  "payments": [
    {
      "id": 1,
      "provider__cnpj": 1,
      "date_issuance": "2019-10-01",
      "date_due": "2019-10-01",
      "date_anticipation": "2019-09-15",
      "value_original": 1000.0,
      "discount": 16.0,
      "value_with_discount": 984.0,
      "status": "AGUAR",
      "created_at": "2022-06-26T22:14:36.749954Z",
      "updated_at": "2022-06-27T18:52:20.563004Z"
    },
    {
      "id": 2,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": "2022-07-15",
      "value_original": 156.0,
      "discount": 1.56,
      "value_with_discount": 154.44,
      "status": "APROV",
      "created_at": "2022-06-26T22:14:48.121456Z",
      "updated_at": "2022-06-27T18:52:37.286695Z"
    },
    {
      "id": 3,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": "2022-07-24",
      "value_original": 4650.0,
      "discount": 4.65,
      "value_with_discount": 4645.35,
      "status": "NEGAD",
      "created_at": "2022-06-26T22:14:56.239657Z",
      "updated_at": "2022-06-27T18:52:48.313093Z"
    },
    {
      "id": 4,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": null,
      "value_original": 98789.0,
      "discount": null,
      "value_with_discount": null,
      "status": "DISPO",
      "created_at": "2022-06-26T22:15:06.115609Z",
      "updated_at": "2022-06-27T18:39:11.135126Z"
    },
    {
      "id": 5,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-06-27",
      "date_anticipation": null,
      "value_original": 98.8,
      "discount": null,
      "value_with_discount": null,
      "status": "INDIS",
      "created_at": "2022-06-26T22:15:16.424598Z",
      "updated_at": "2022-06-27T18:53:57.131479Z"
    }
  ]
}
```

### /pagamentos/DISPO/

Retona todos os pagamentos do usuário **DISPONÍVEIS** para adiantamento.

Requisição

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/DISPO/
```

Resposta

```json
{
  "count": 1,
  "payments": [
    {
      "id": 4,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": null,
      "value_original": 98789.0,
      "discount": null,
      "value_with_discount": null,
      "status": "DISPO",
      "created_at": "2022-06-26T22:15:06.115609Z",
      "updated_at": "2022-06-27T18:39:11.135126Z"
    }
  ]
}
```

### /pagamentos/INDIS/

Retona todos os pagamentos do usuário **INDISPONÍVEIS** para adiantamento.

Requisição

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/INDIS/
```

Resposta

```json
{
  "count": 1,
  "payments": [
    {
      "id": 5,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-06-27",
      "date_anticipation": null,
      "value_original": 98.8,
      "discount": null,
      "value_with_discount": null,
      "status": "INDIS",
      "created_at": "2022-06-26T22:15:16.424598Z",
      "updated_at": "2022-06-27T18:53:57.131479Z"
    }
  ]
}
```

### /pagamentos/AGUAR/

Retona todos os pagamentos do usuário **AGUARDANDO CONFIRMAÇÃO** para adiantamento.

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/AGUAR/
```

Resposta

```json
{
  "count": 1,
  "payments": [
    {
      "id": 1,
      "provider__cnpj": 1,
      "date_issuance": "2019-10-01",
      "date_due": "2019-10-01",
      "date_anticipation": "2019-09-15",
      "value_original": 1000.0,
      "discount": 16.0,
      "value_with_discount": 984.0,
      "status": "AGUAR",
      "created_at": "2022-06-26T22:14:36.749954Z",
      "updated_at": "2022-06-27T18:52:20.563004Z"
    }
  ]
}
```

### /pagamentos/APROV/

Retona todos os pagamentos do usuário **APROVADOS** para adiantamento.

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/APROV/
```

Resposta

```json
{
  "count": 1,
  "payments": [
    {
      "id": 2,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": "2022-07-15",
      "value_original": 156.0,
      "discount": 1.56,
      "value_with_discount": 154.44,
      "status": "APROV",
      "created_at": "2022-06-26T22:14:48.121456Z",
      "updated_at": "2022-06-27T18:52:37.286695Z"
    }
  ]
}
```

### /pagamentos/NEGAD/

Retona todos os pagamentos do usuário **NEGADOS** para adiantamento.

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/pagamentos/NEGAD/
```

Resposta

```json
{
  "count": 1,
  "payments": [
    {
      "id": 3,
      "provider__cnpj": 1,
      "date_issuance": "2022-06-26",
      "date_due": "2022-07-25",
      "date_anticipation": "2022-07-24",
      "value_original": 4650.0,
      "discount": 4.65,
      "value_with_discount": 4645.35,
      "status": "NEGAD",
      "created_at": "2022-06-26T22:14:56.239657Z",
      "updated_at": "2022-06-27T18:52:48.313093Z"
    }
  ]
}
```

---

### /solicitar-adiantamento/ID_PAGAMENTO/DATA_ANTECIPAÇÃO/

Solicita o adiantamento para o **ID_PAGAMENTO** para a **DATA_ANTECIPAÇÃO**.

O Formato usado em DATA_ANTECIPAÇÃO é ANO-MES-DIA, ou seja, **2020-05-30**.

Requisição

```shell
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ACCESS_TOKEN" \
  http://localhost:8000/api/solicitar-adiantamento/1/2019-09-15/
```

Resposta

```json
{
  "payment": {
    "id": 1,
    "provider_cnpj": 1,
    "date_issuance": "2019-10-01",
    "date_due": "2019-10-01",
    "date_anticipation": "2019-09-15",
    "value_original": 1000.0,
    "discount": 16.0,
    "value_with_discount": 984.0,
    "status": "AGUAR",
    "created_at": "2022-06-26T22:14:36.749954Z",
    "updated_at": "2022-06-27T19:02:52.097965Z"
  }
}
```