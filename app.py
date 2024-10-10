from flask import Flask, request, jsonify, render_template
from database.mongodb import test_connection
from controllers.bot_controller import bot_blueprint
import json

app = Flask(__name__)

# Testar a conexão
test_connection()

# Registrar o blueprint do bot
app.register_blueprint(bot_blueprint)

# Carregar dados do curso
with open('curso_info.json', 'r', encoding='utf-8') as f:
    curso = json.load(f)

# Dicionário para armazenar o progresso dos usuários
progresso_usuarios = {}

def processar_mensagem(numero_usuario, mensagem):
    if numero_usuario not in progresso_usuarios:
        return iniciar_curso(numero_usuario)
    else:
        return continuar_curso(numero_usuario, mensagem)

def iniciar_curso(numero_usuario):
    progresso_usuarios[numero_usuario] = {
        "modulo_atual": 0,
        "licao_atual": 0
    }
    mensagem = f"Bem-vindo ao curso de Informática Básica, usuário {numero_usuario}! Escolha um módulo:\n"
    for i, modulo in enumerate(curso["modulos"]):
        mensagem += f"{i+1}. {modulo['nome']}\n"
    return mensagem

def continuar_curso(numero_usuario, mensagem):
    progresso = progresso_usuarios[numero_usuario]
    # Aqui você implementaria a lógica para avançar no curso
    # Por enquanto, vamos apenas retornar uma mensagem genérica
    return f"Continuando o curso para o usuário {numero_usuario}. Sua mensagem: {mensagem}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/enviar_mensagem", methods=["POST"])
def enviar_mensagem():
    dados = request.json
    numero_usuario = dados["numero"]
    mensagem = dados["mensagem"]
    resposta = processar_mensagem(numero_usuario, mensagem)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(debug=True)