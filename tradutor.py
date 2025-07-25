from deep_translator import GoogleTranslator

def traduzir(texto, de='en', para='pt'):
    try:
        resultado = GoogleTranslator(source=de, target=para).translate(texto)
        return resultado
    except Exception as e:
        return f"Erro ao traduzir: {e}"