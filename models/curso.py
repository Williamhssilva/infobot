from config import CURSO

class Curso:
    @staticmethod
    def get_modulos():
        return CURSO['modulos']

    @staticmethod
    def get_modulo(index):
        return CURSO['modulos'][index]

    @staticmethod
    def get_licao(modulo_index, licao_index):
        return CURSO['modulos'][modulo_index]['licoes'][licao_index]
