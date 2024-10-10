from flask import Blueprint, request, jsonify, render_template
from models.curso import Curso
from models.usuario import Usuario
from views.bot_view import BotView

bot_blueprint = Blueprint('bot', __name__)

@bot_blueprint.route('/')
def home():
    return render_template('index.html')

@bot_blueprint.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.json
    numero_usuario = dados['numero']
    mensagem = dados['mensagem']

    usuario = Usuario.criar_ou_obter(numero_usuario)
    progresso = Usuario.obter_progresso(numero_usuario)

    if progresso['modulo'] == -1:  # Usuário ainda não escolheu um módulo
        try:
            modulo_escolhido = int(mensagem) - 1  # Converte a escolha do usuário para índice
            if 0 <= modulo_escolhido < len(Curso.get_modulos()):
                Usuario.atualizar_progresso(numero_usuario, modulo_escolhido, 0)
                modulo = Curso.get_modulo(modulo_escolhido)
                licao = Curso.get_licao(modulo_escolhido, 0)
                resposta = f"Ótimo! Você escolheu o módulo '{modulo['nome']}'.\n\n"
                resposta += BotView.formatar_licao(licao)
            else:
                resposta = "Opção inválida. Por favor, escolha um número de módulo válido."
        except ValueError:
            resposta = "Por favor, digite o número do módulo que deseja estudar."
    else:
        licao = Curso.get_licao(progresso['modulo'], progresso['licao'])

        if mensagem.lower() == 'próximo':
            progresso['licao'] += 1
            if progresso['licao'] >= len(Curso.get_modulo(progresso['modulo'])['licoes']):
                progresso['licao'] = 0
                progresso['modulo'] += 1
                if progresso['modulo'] >= len(Curso.get_modulos()):
                    progresso['modulo'] = -1  # Volta para a seleção de módulos
                    resposta = "Parabéns! Você completou todos os módulos. Escolha um módulo para revisar:\n"
                    resposta += BotView.listar_modulos()
                else:
                    modulo = Curso.get_modulo(progresso['modulo'])
                    resposta = f"Iniciando novo módulo: {modulo['nome']}\n\n"
            
            if progresso['modulo'] != -1:
                Usuario.atualizar_progresso(numero_usuario, progresso['modulo'], progresso['licao'])
                licao = Curso.get_licao(progresso['modulo'], progresso['licao'])
                resposta += BotView.formatar_licao(licao)
        else:
            resposta = BotView.formatar_pergunta(licao['questionario'][0])

    return jsonify({'resposta': resposta})