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

def cadastrar_usuario():
  nome = input("Digite o nome: ")
  idade = input("Digite a idade: ")
  email = input("Digite o email: ")
  senha = input("Digite a senha: ")

  cursor.execute("INSERT INTO usuarios (nome, idade, email, senha) VALUES (?,?,?,?)", (nome, idade, email, senha))
  conn.commit()
  print(f"usuário {nome} cadastrado com sucesso!\n")

def deletar():
  nome = input("Digite o nome do usuário: ")
  cursor.execute("DELETE FROM usuarios WHERE nome = ?", (nome,))
  try:
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
      print(f"- ID {usuario[0]} | Nome: {usuario[1]} | Idade: {usuario[2]} | E-mail: {usuario[3]}")
    print()

def menu():
  while True:
    print("=== Menu ===")
    print("1. cadastrar user")
    print("2. deletar user")
    print("3. listar users")
    print("4. sair")
    opcao = input("escolha uma opção: ")

    if opcao == "1":
      cadastrar_usuario()
    elif opcao == "3":
      listar_usuario()
    elif opcao == "2":
      deletar()
    elif opcao == "4":
      print("saindo...")
      break
    else:
      print("opção inválida! tente novamente.")

menu()

conn.close()