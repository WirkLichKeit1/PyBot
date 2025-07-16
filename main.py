from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from codigo import codigo
from tradutor import traduzir
from chat import responder, take_intencao
import sqlite3

app = Flask(__name__)
app.secret_key = "TXGKPOYW"

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def verificar_login():
    usuario = request.form.get("usuario", "").strip()
    senha = request.form.get("senha", "").strip()

    conn = sqlite3.connect("teste3.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado:
        return redirect("/menu")
    else:
        return render_template("login.html", erro="usuario ou senha incorretos!")

@app.route("/cadastro", methods=["GET","POST"])
def cadastrarUsuario():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()
        email = request.form.get("email", "").strip()

        if not usuario or not senha or not email:
            flash("preencha todos os campos.", "erro")
            return redirect("/cadastro")

        try:
            conn = sqlite3.connect("teste3.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (nome, idade, email, senha) VALUES (?, ?, ?, ?)", (usuario, None, email, senha))
            conn.commit()
            conn.close()
            flash("cadastro realizado com sucesso!", "sucesso")
            return redirect("/")

        except sqlite3.IntegrityError:
            flash("Este e-mail ou nome de usuário já está cadastrado.", "erro")
            return redirect("/cadastro")

        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", "erro")
            return redirect("/cadastro")
    
    return render_template("cadastro.html")
    
@app.route("/menu")
def home():
    return render_template("index.html")

@app.route("/tradutor")
def tradutor():
    return render_template("tradutor.html")

@app.route("/codigo")
def codigo_func():
    return render_template("codigo.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/codigo/gerar", methods=["GET"])
def gerar_codigo():
    return jsonify({"codigo": codigo()})

@app.route("/traduzir", methods=["POST"])
def rota_traduzir():
    data = request.get_json()
    texto = data.get("texto", "")
    origem = data.get("de", "en")
    destino = data.get("para", "pt")
    resultado = traduzir(texto, de=origem, para=destino)
    return jsonify({"traducao": resultado})

@app.route("/chat", methods=["POST"])
def rota_chat():
    data = request.get_json()
    mensagem = data.get("mensagem", "")
    intencao = take_intencao(mensagem)
    resposta = responder(intencao, mensagem)
    return jsonify({"resposta": resposta})