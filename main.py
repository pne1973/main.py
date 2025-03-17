import telebot
import sqlite3
import requests

TOKEN = "7717065833:AAExaSLGfyH3DpMQN96aMx5627p_jUnbM4Y"
ADSTERRA_API = "SUA_ADSTERRA_API_KEY"  # Substitua pela chave correta da Adsterra

bot = telebot.TeleBot(TOKEN)

# Conectar ao banco de dados SQLite
conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabelas se não existirem
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        balance REAL DEFAULT 0
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ad_views (
        user_id INTEGER,
        ad_link TEXT UNIQUE
    )
""")
conn.commit()

# Função para buscar anúncio da Adsterra
def pegar_anuncio_adsterra():
    try:
        response = requests.get(f"https://www.adsterrra.com/api/v3/{ADSTERRA_API}")
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                return data[0].get("url", None), data[0].get("title", "Anúncio")
            else:
                return None, None
        else:
            print(f"Erro ao buscar anúncio: {response.status_code}, {response.text}")
            return None, None
    except Exception as e:  # ADICIONE ESTE except PARA EVITAR O ERRO DE SYNTAXE
        print(f"Erro na requisição da Adsterra: {str(e)}")
        return None, None  # Retorno para evitar erro de sintaxe
       
