# Possui as rotas

from app import app

@app.route("/")
def home():
    return "API de Tarefas rodando com estrutura modular!"
