# Inicializa o Flask e carregas as rotas
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'primeira-chave'
jwt = JWTManager(app)

@jwt.unauthorized_loader
def erro_autenticacao_customizado(mensagem):
    print("JWT bloqueou a requisição:", mensagem)
    return jsonify({"erro": "Token ausente ou inválido"}), 401

# Inicializa o banco
db = SQLAlchemy(app)

from app import auth, models, routes, tarefas
