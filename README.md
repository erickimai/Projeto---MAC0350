# Gerenciador de Tarefas

Um aplicativo web simples para gerenciar tarefas organizadas por categorias, construído com **FastAPI**, **HTMX** e **SQLite**.

## Funcionalidades

- ✅ Criar, ler, atualizar e deletar tarefas
- 📁 Organizar tarefas por categorias
- 🔍 Buscar e filtrar tarefas por nome ou categoria
- ⚡ Atualizações em tempo real com HTMX (sem recarregar a página)
- 📱 Totalmente responsivo (mobile e desktop)

## Stack Tecnológico

- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: HTML5, CSS3, HTMX
- **Servidor**: Uvicorn

## Configuração

### Pré-requisitos

- Python 3.10+
- pip

### Instalação

1. Clone o repositório
   ```bash
   git clone <sua-url-do-repo>
   cd taskmanager
   ```

2. Crie e ative um ambiente virtual
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências
   ```bash
   pip install -r requirements.txt
   ```

4. Execute o servidor
   ```bash
   uvicorn main:app --reload
   ```

O aplicativo estará disponível em `http://127.0.0.1:8000`

## Estrutura do Projeto

```
taskmanager/
├── main.py              # App FastAPI & rotas
├── models.py            # Modelos SQLAlchemy
├── database.py          # Configuração do banco de dados
├── requirements.txt     # Dependências
├── templates/           # Templates Jinja2
│   ├── base.html
│   ├── index.html
│   ├── manage.html
│   └── partials/        # Fragmentos HTMX
└── static/
    └── style.css        # Estilos responsivos
```

## Uso

1. Vá para **Manage** para criar categorias e tarefas
2. Visualize todas as tarefas na página **Home**
3. Use a barra de busca para encontrar tarefas por nome
4. Filtre por categoria usando o dropdown
5. Edite tarefas inline ou delete-as com o botão de delete

## Endpoints da API

| Método | Caminho | Descrição |
|--------|---------|-----------|
| GET | `/` | Página inicial com lista de tarefas |
| GET | `/manage` | Página de gerenciamento para CRUD |
| GET | `/tasks` | Buscar/filtrar tarefas (HTMX) |
| POST | `/tasks` | Criar uma tarefa |
| PUT | `/tasks/{id}` | Atualizar título da tarefa |
| DELETE | `/tasks/{id}` | Deletar uma tarefa |
| POST | `/categories` | Criar uma categoria |
| DELETE | `/categories/{id}` | Deletar uma categoria |

## Banco de Dados

O aplicativo usa SQLite com dois modelos:

- **Category**: agrupa tarefas por assunto/projeto
- **Task**: pertence a uma categoria (relacionamento Um-para-Muitos)

## Licença

MIT
