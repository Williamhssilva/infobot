from database.mongodb import usuarios_collection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Usuario:
    @staticmethod
    def criar_ou_obter(numero):
        usuario = usuarios_collection.find_one({"numero": numero})
        if not usuario:
            usuario = {
                "numero": numero,
                "modulo_atual": -1,  # Inicializa com -1
                "licao_atual": 0
            }
            result = usuarios_collection.insert_one(usuario)
            logger.info(f"Novo usuário criado: {numero}, ID: {result.inserted_id}")
        else:
            logger.info(f"Usuário existente recuperado: {numero}")
        return usuario

    @staticmethod
    def atualizar_progresso(numero, modulo, licao):
        result = usuarios_collection.update_one(
            {"numero": numero},
            {"$set": {"modulo_atual": modulo, "licao_atual": licao}}
        )
        logger.info(f"Progresso atualizado para usuário {numero}: módulo {modulo}, lição {licao}. Modificados: {result.modified_count}")

    @staticmethod
    def obter_progresso(numero):
        usuario = usuarios_collection.find_one({"numero": numero})
        if usuario:
            logger.info(f"Progresso obtido para usuário {numero}: módulo {usuario['modulo_atual']}, lição {usuario['licao_atual']}")
        else:
            logger.warning(f"Usuário não encontrado: {numero}")
        return {
            "modulo": usuario["modulo_atual"] if usuario else -1,
            "licao": usuario["licao_atual"] if usuario else 0
        }