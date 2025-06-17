# Possui as rotas

from flask import jsonify, request
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import Tarefa, Usuario


@app.route("/")
def home():
    return "API de Tarefas rodando com estrutura modular!"
