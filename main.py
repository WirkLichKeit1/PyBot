from flask import Flask, render_template, jsonify, request, redirect, url_for, flash, session
from codigo import codigo
from tradutor import traduzir
from chat import responder, take_intencao
import sqlite3

app = Flask(__name__)
app.secret_key = "TXGKPOYW"

@app.route("/")
def cadastro():
    return render_template("cadastro.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrarUsuario():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()
        email = request.form.get("email", "").strip()

        if not usuario or not senha or not email:
            flash("Preencha todos os campos.", "erro")
            return redirect("/cadastro")

        try:
            conn = sqlite3.connect("teste3.db")
            cursor = conn.cursor()
            cursor.execute("SELECT email, senha FROM usuarios")
            users = cursor.fetchall()

            if any(email == u[0] for u in users):
                flash("Este e-mail já está sendo usado por outro usuário.", "erro")
                conn.close()
                return redirect("/cadastro")
            elif any(senha == u[1] for u in users):
                flash("Esta senha já está sendo usada por outro usuário.", "erro")
                conn.close()
                return redirect("/cadastro")

            cursor.execute(
                "INSERT INTO usuarios (nome, idade, email, senha) VALUES (?, ?, ?, ?)",
                (usuario, None, email, senha)
            )

            conn.commit()
            conn.close()
            flash("Cadastro realizado com sucesso!", "sucesso")
            return redirect("/login")

        except sqlite3.IntegrityError:
            flash("Este e-mail ou nome de usuário já está cadastrado.", "erro")
            return redirect("/cadastro")

        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", "erro")
            return redirect("/cadastro")

    return render_template("cadastro.html")

@app.route("/login", methods=["GET", "POST"])
def verificar_login():
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "").strip()

        conn = sqlite3.connect("teste3.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ?", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            session["usuario_id"] = resultado[0]
            session["nome"] = resultado[1]
            session["email"] = resultado[3]
            return redirect("/menu")
        else:
            flash("Usuário ou senha incorretos.", "erro")
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect("/login")

@app.route("/perfil")
def perfil():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("perfil.html", nome=session.get("nome"), email=session.get("email"))

@app.route("/menu")
def home():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/tradutor")
def tradutor():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("tradutor.html")

@app.route("/codigo")
def codigo_func():
    if "usuario_id" not in session:
        return redirect("/login")
    return render_template("codigo.html")

@app.route("/chat")
def chat():
    if "usuario_id" not in session:
        return redirect("/login")
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
