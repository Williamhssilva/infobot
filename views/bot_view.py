from models.curso import Curso

class BotView:

    @staticmethod
    def formatar_mensagem(conteudo):
        return f"InfoBot: {conteudo}"

    @staticmethod
    def mensagem_boas_vindas(nome_modulo):
        return f"Bem-vindo ao módulo '{nome_modulo}'! Vamos começar?"

    @staticmethod
    def formatar_licao(licao):
        return f"Lição: {licao['titulo']}\n\n{licao['conteudo']}\n\nMaterial de apoio: {licao['material_apoio']}"

    @staticmethod
    def formatar_pergunta(pergunta):
        opcoes = "\n".join(pergunta['opcoes'])
        return f"Pergunta: {pergunta['pergunta']}\n\nOpções:\n{opcoes}"

    @staticmethod
    def listar_modulos():
        modulos = Curso.get_modulos()
        lista = "Escolha um módulo:\n"
        for i, modulo in enumerate(modulos, 1):
            lista += f"{i}. {modulo['nome']}\n"
        return lista