from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from app import app, db
from app.models import Tarefa


@app.route("/tarefas", methods=["POST"])
@jwt_required()
def criar_tarefa():
    # Obtém os dados enviados na requisição
    dados = request.get_json()

    # Busca o ID do usuário autenticado pelo JWT
    usuario_id = int(get_jwt_identity())

    # Extrai os dados da nova tarefa
    titulo = dados.get("titulo")
    descricao = dados.get("descricao", "")
    status = dados.get("status", "pendente")

    # Cria nova instância de Tarefa vinculada a um usuário
    nova_tarefa = Tarefa(titulo=titulo, 
                         descricao=descricao, 
                         status=status, 
                         usuario_id=usuario_id)
    
    # Salva tarefa no banco de dados
    db.session.add(nova_tarefa)
    db.session.commit()

    # return jsonify({"mensagem": "Tarefa adicionada com sucesso"})

    # Retorna os dados da nova tarefa
    return jsonify({
        "id": nova_tarefa.id,
        "titulo": nova_tarefa.titulo,
        "descricao": nova_tarefa.descricao,
        "status": nova_tarefa.status
    }), 201