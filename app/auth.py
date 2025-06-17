from flask import jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from app import app, db
from app.models import Usuario


# Cria endpoint /register para registrar usuário
@app.route("/register", methods=["POST"])
def register():
    dados = request.get_json()
    print("Dados recebidos:", dados)

    nome = dados.get("nome")
    email = dados.get("email")
    senha = dados.get("senha")

    if not nome or not email or not senha:
        return jsonify({"erro": "Dados incompletos"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"erro": "Email já cadastrado"}), 400

    senha_hash = generate_password_hash(senha)
    novo_usuario = Usuario(nome=nome, email=email, senha_hash=senha_hash)

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"mensagem": "Usuário criado com sucesso"}), 201


# Cria endpoint /login para fazer login do usuário
@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json()

    email = dados.get("email")
    senha = dados.get("senha")

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario or not check_password_hash(usuario.senha_hash, senha):
        return jsonify({"erro": "Email ou senha inválidos"})
    
    token = create_access_token(identity=str(usuario.id))

    return jsonify({"access_token": token}), 200


@app.route("/perfil", methods=["GET"])
@jwt_required()
def perfil():
    usuario_id = int(get_jwt_identity())
    usuario = Usuario.query.get(usuario_id)

    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    return jsonify({
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email
    }), 200
