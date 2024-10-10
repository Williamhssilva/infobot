from pymongo import MongoClient
from config import MONGODB_URI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = None
db = None
usuarios_collection = None

def init_db():
    global client, db, usuarios_collection
    try:
        client = MongoClient(MONGODB_URI)
        db = client.infobot_db
        usuarios_collection = db.usuarios
        logger.info("Conexão com MongoDB inicializada")
    except Exception as e:
        logger.error(f"Erro ao inicializar conexão com MongoDB: {e}")

def test_connection():
    try:
        client.admin.command('ping')
        logger.info("Conexão com MongoDB bem-sucedida!")
        return True
    except Exception as e:
        logger.error(f"Erro na conexão com MongoDB: {e}")
        return False

# Inicialize a conexão quando este módulo for importado
init_db()