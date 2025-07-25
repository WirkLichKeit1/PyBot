import sqlite3

conn = sqlite3.connect("teste3.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    idade INTEGER,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
    )
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    remetente_id INTEGER NOT NULL,
    destinatario_id INTEGER NOT NULL,
    mensagem TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (remetente_id) REFERENCES usuarios(id),
    FOREIGN KEY (destinatario_id) REFERENCES usuarios(id)
)
""")

conn.commit()

def cadastrar_usuario():
  nome = input("Digite o nome: ")
  idade = input("Digite a idade: ")
  email = input("Digite o email: ")
  senha = input("Digite a senha: ")

  cursor.execute("SELECT email, senha FROM usuarios")
  user_x = cursor.fetchall()

  if any(email == u[0] for u in user_x):
    print("email já existente.")
  elif any(senha == u[1] for u in user_x):
    print("Essa senha já está sendo usado por outro usuário.")
  else:
    cursor.execute("INSERT INTO usuarios (nome, idade, email, senha) VALUES (?,?,?,?)", (nome, idade, email, senha))
    conn.commit()
    print(f"usuário {nome} cadastrado com sucesso!\n")

def deletar():
  nome = input("Digite o nome do usuário: ")
  cursor.execute("DELETE FROM usuarios WHERE nome = ?", (nome,))
  try:
    cursor.execute("SELECT * FROM usuarios")
    usuario = cursor.fetchall()
    if not usuario:
      print("usuário inexistente.")
      return
    else:
      conn.commit()
      print(f"usuário {nome} deletado com sucesso!\n")

  except Exception as e:
    print(f"ERRO: {e}")

def listar_usuario():
  cursor.execute("SELECT * FROM usuarios")
  usuarios = cursor.fetchall()

  if not usuarios:
    print("não existem usuários cadastrados.")
  else:
    print("LISTA:")
    for usuario in usuarios:
      print(f"- ID {usuario[0]} | Nome: {usuario[1]} | Idade: {usuario[2]} | E-mail: {usuario[3]} Senha: {usuario[4]}")
    print()

def listar_msgs():
  cursor.execute("SELECT * FROM mensagens")
  mensagens = cursor.fetchall()
  
  if not mensagens:
    print("sem mensagens...")
  
  print("Lista:")
  for mensagem in mensagens:
    print(f"- ID {mensagem[0]} | remetente: {mensagem[1]} | destinatário: {mensagem[2]} | mensagem: {mensagem[3]} | timestamp: {mensagem[4]}")

def menu():
  while True:
    print("=== Menu ===")
    print("1. cadastrar user")
    print("2. deletar user")
    print("3. listar users")
    print("5. listar msgs")
    print("4. sair")
    opcao = input("escolha uma opção: ")

    if opcao == "1":
      cadastrar_usuario()
    elif opcao == "3":
      listar_usuario()
    elif opcao == "2":
      deletar()
    elif opcao == "5":
      listar_msgs()
    elif opcao == "4":
      print("saindo...")
      break
    else:
      print("opção inválida! tente novamente.")

menu()

conn.close()