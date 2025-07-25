import sqlite3
from datetime import datetime

DB_PATH = "teste3.db"

def conectar():
    return sqlite3.connect(DB_PATH)

def enviar_mensagens(remetente_id, destinatario_id, mensagem):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO mensagens (remetente_id, destinatario_id, mensagem, timestamp)
        VALUES (?, ?, ?, ?)
    """, (remetente_id, destinatario_id, mensagem, datetime.now()))
    conn.commit()
    conn.close()

def listar_mensagens(usuario_id, contato_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT remetente_id, destinatario_id, mensagem, timestamp FROM mensagens WHERE (remetente_id = ? AND destinatario_id = ?)
        OR (remetente_id = ? AND destinatario_id = ?)
        ORDER BY timestamp ASC
    """, (usuario_id, contato_id, contato_id, usuario_id))
    mensagens = cursor.fetchall()
    conn.close()
    return mensagens

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def obter_nome_usuario(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome FROM usuarios WHERE id = ?", (user_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Desconhecido"