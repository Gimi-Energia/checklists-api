# Checklists API

A Checklists API foi desenhada para facilitar a gestão de envios de checklists para os clientes.

## ✔️ Tecnologias usadas
- Python
- Django
- Django Rest Framework
- PostgreSQL
- Simple JWT
- Swagger/Redoc
- Vercel
- ReportLab Toolkit

## 📁 Acesso ao deploy

[![Deploy with Vercel](https://vercel.com/button)](https://checklists-api.vercel.app/)

## 🔨 Funcionalidades

- **Autenticação**: Sistema de tokens para acesso seguro à API.
- **Gestão de Usuários**: Administração de usuários que podem acessar a API.
- **Gestão de Checklists**: Gerencie as listas e os checklists relacionados a estas.
- **Autenticação**: Sistema de tokens para acesso seguro à API.
- **Notificações**: Notificações por e-mail com arquivos PDF.

## 📌 Uso

A Checklists API segue os princípios REST para comunicação. Os seguintes endpoints estão disponíveis:

### /registrations/
- Gerenciar checklist Dados Cadastrais e realizar operações CRUD.

### /checklist/a/
- Gerenciar checklist A e realizar operações CRUD.

### /checklist/b/
- Gerenciar checklist B e realizar operações CRUD.

### /checklist/c/
- Gerenciar checklist C e realizar operações CRUD.

### /checklist/d/
- Gerenciar checklist D e realizar operações CRUD.

### /checklist/e/
- Gerenciar checklist E e realizar operações CRUD.

### /checklist/f/
- Gerenciar checklist F e realizar operações CRUD.

### /checklist/g/
- Gerenciar checklist G e realizar operações CRUD.

### /checklists/
- Gerenciar checklists gerais e realizar operações CRUD.

### /checklists/add_products/
- Adicionar produtos a um checklist específico.

### /checklists/register_answer/
- Registrar uma resposta para um checklist específico.

### /checklists/remove_products/
- Remover produtos de um checklist específico.

### /checklists/update_products/
- Atualizar produtos em um checklist específico.

### /products/
- Gerenciar produtos e realizar operações CRUD.

### /users/
- Gerenciar usuários e realizar operações CRUD.

## 🔐 Autenticação

A autenticação é realizada através de JWT. Utilize a rota `/token/` para obter um token de acesso, enviando as credenciais do usuário. Utilize este token nas requisições subsequentes para autenticar.

## 🛠️ Abrindo e rodando o projeto

Para configurar a Requisitions API em seu ambiente, siga estas etapas:

1. Clone o repositório do projeto para sua máquina local.
2. Configure o ambiente virtual para Python e ative-o.
3. Instale as dependências do projeto
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente necessárias para a conexão com o banco de dados e outras configurações de sistema.
5. Execute as migrações do banco de dados
```bash
python manage.py migrate
```
6. Crie um super usuário para ter acesso a `/admin/`
```bash
python manage.py createsuperuser
```
7. Inicie o servidor de desenvolvimento
```bash
python manage.py runserver
```
