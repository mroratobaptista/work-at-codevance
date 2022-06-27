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
### Copiar arquivo para .env
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
### Configuração Inicial
1. Acesse [Django Admin](http:127.0.0.1:8000/admin).
2. Crie 2 grupos.
   1. Operador
   2. Fornecedor
3. Inclua o grupo Operador no usuário Admin criado anteriormente e/ou em outro usuário que gostaria.
4. Crie os usuários dos fornecedores e adicione o grupo Fornecedor em cada um deles.
5. Crie os fornecedores e selecione seus respectivos usuários.
6. Crie os pagamentos e selecione aos respectivos fornecedores.