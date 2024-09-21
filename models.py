from flask_login import UserMixin
import mysql.connector
from mysql.connector import Error

BANCO_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'seu_banco'
}

def obter_conexao():
    try:
        conn = mysql.connector.connect(**BANCO_CONFIG)
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

# modelo de usuário
class User(UserMixin):
    id: str

    def __init__(self, email, senha):
        self.email = email
        self.senha = senha

    @classmethod
    def get(cls, id):
        conn = obter_conexao()
        if conn:
            SLCT = 'SELECT * FROM usuarios WHERE id = %s'
            cursor = conn.cursor(dictionary=True)
            cursor.execute(SLCT, (id,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                user = User(dados['email'], dados['senha'])
                user.id = dados['id']
                return user
        return None

    @classmethod
    def get_by_email(cls, email):
        conn = obter_conexao()
        if conn:
            SLCT = 'SELECT * FROM usuarios WHERE email = %s'
            cursor = conn.cursor(dictionary=True)
            cursor.execute(SLCT, (email,))
            dados = cursor.fetchone()
            cursor.close()
            conn.close()
            if dados:
                user = User(dados['email'], dados['senha'])
                user.id = dados['id']
                return user
        return None
    
    def save(self):        
        conn = obter_conexao()  
        if conn:
            cursor = conn.cursor()
            try:
                # Corrigido para ter apenas dois valores
                cursor.execute("INSERT INTO usuarios(email, senha) VALUES (%s, %s)", (self.email, self.senha))
                # Salva o id no objeto recém salvo no banco
                self.id = cursor.lastrowid  # Use 'self.id' em vez de 'self._id'
                conn.commit()
            except Exception as e:
                print(f"Erro ao salvar usuário: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
            return True
        return False
    @classmethod
    def exists(cls, email):
        conn = obter_conexao()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return user is not None  # Retorna True se o usuário existir, caso contrário, False
        return False  # Retorna False se não conseguir conectar