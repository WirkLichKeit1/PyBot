import requests
from random import choice
from langdetect import detect
from deep_translator import GoogleTranslator
import spacy
import unicodedata

nlp = spacy.load("pt_core_news_sm")

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    return texto

def extrair_palavras_chave(texto):
    doc = nlp(texto)
    return [token.text for token in doc if token.pos_ in ["NOUN", "PROPN", "VERB"] and not token.is_stop]

def detectar_idioma(texto):
    try:
        return detect(texto)
    except:
        return "pt"

def traduzir(texto, origem="auto", destino="pt"):
    try:
        return GoogleTranslator(source=origem, target=destino).translate(texto)
    except:
        return texto

def pesquisar_wolfram(pergunta_en, app_id):
    url = f"http://api.wolframalpha.com/v1/result?i={requests.utils.quote(pergunta_en)}&appid={app_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return ""
    except:
        return ""

def pesquisar_google(pergunta_en, cx, api_key):
    url = f"https://www.googleapis.com/customsearch/v1?q={pergunta_en}&cx={cx}&key={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if "items" in data:
            return data["items"][0]["snippet"]
        return ""
    except:
        return ""

def pesquisar_duckduckgo(pergunta_en):
    url = f"https://api.duckduckgo.com/?q={pergunta_en}&format=json&no_redirect=1&skip_disambig=1"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("AbstractText"):
            return data["AbstractText"]
        elif data.get("RelatedTopics"):
            for item in data["RelatedTopics"]:
                if isinstance(item, dict) and "Text" in item:
                    return item["Text"]
        return ""
    except:
        return ""

def pesquisar_wikipedia(pergunta_en):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{pergunta_en.replace(' ', '_')}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("extract", "")
        return ""
    except:
        return ""

def resposta_util(resposta, minimo=350):
    """Verifica se a resposta é longa o suficiente para ser útil."""
    return resposta and len(resposta.strip()) >= minimo

def take_intencao(mensagem):
    mensagem_limpa = normalizar_texto(mensagem)
    palavras = mensagem_limpa.split()

    saudacoes = ["oi", "ola", "e ai", "boa noite", "bom dia", "boa tarde", "eae", "hello"]
    if any(palavra in saudacoes for palavra in palavras):
        return "saudacao"
    elif "tudo bem" in mensagem_limpa or "como voce esta" in mensagem_limpa:
        return "status"
    elif "seu nome" in mensagem_limpa or "como se chama" in mensagem_limpa:
        return "nome"
    elif "faz" in mensagem_limpa or "para que serve" in mensagem_limpa:
        return "funcao"
    elif "adeus" in mensagem_limpa or "tchau" in mensagem_limpa:
        return "despedida"
    else:
        return "conhecimento"

respostas = {
    "saudacao": ["Oi! Tudo certo?", "Olá, como posso ajudar?", "Seja bem-vindo! O que deseja saber?"],
    "status": ["Estou ótimo, obrigado por perguntar!", "Tudo bem por aqui! E com você?"],
    "nome": ["Eu não tenho um nome. Sou apenas um bot simples feito em Python por um dev qualquer."],
    "funcao": ["Eu converso com você e respondo perguntas simples e curiosidades."],
    "despedida": ["Tchau! Até a próxima.", "Até logo!"],
    "desconhecida": ["Desculpe, ainda não sei responder isso.", "Foi mal, ainda não aprendi a responder essa pergunta."]
}

# Suas credenciais:
WOLFRAM_APP_ID = "WHG9HP-PUWYR56HH6"
GOOGLE_CX = "c2be31e3cb9124b92"
GOOGLE_API_KEY = "AIzaSyD7MdJxivTecnxXQkWPeNW87ozvtDTmj5A"

def responder(intencao, mensagem):
    if intencao == "conhecimento":
        idioma = detectar_idioma(mensagem)
        pergunta_en = traduzir(mensagem, origem=idioma, destino="en")

        fontes = [
            lambda: pesquisar_wolfram(pergunta_en, WOLFRAM_APP_ID),
            lambda: pesquisar_google(pergunta_en, GOOGLE_CX, GOOGLE_API_KEY),
            lambda: pesquisar_duckduckgo(pergunta_en),
            lambda: pesquisar_wikipedia(pergunta_en)
        ]

        resposta_en = ""
        for fonte in fontes:
            tentativa = fonte()
            if resposta_util(tentativa):
                resposta_en = tentativa
                break

        if resposta_en:
            resposta = traduzir(resposta_en, origem="en", destino="pt") if idioma == "pt" else resposta_en
        else:
            resposta = choice(respostas["desconhecida"])

        return resposta
    else:
        return choice(respostas[intencao])

# Teste local
def Chat():
    print("Digite 'sair' para encerrar.\n")
    while True:
        user_message = input("VOCÊ: ")
        if not user_message:
            print("IA: Nenhuma mensagem foi enviada.")
        elif user_message.lower() == "sair":
            print("IA:", choice(respostas["despedida"]))
            break
        else:
            intencao = take_intencao(user_message)
            resposta = responder(intencao, user_message)
            print("IA:", resposta)