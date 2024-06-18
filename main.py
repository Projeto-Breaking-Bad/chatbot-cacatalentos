import os
import random
import re
from flask import Flask, render_template, request, jsonify
from jinja2 import ChoiceLoader, FileSystemLoader
from transformers import pipeline
import json

app = Flask(__name__)

# Obtém o caminho do diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configura o Flask para usar o caminho relativo ao diretório do script para templates
app.template_folder = os.path.join(script_dir, 'templates')

# Configura o Flask para usar o caminho relativo ao diretório do script para os arquivos estáticos
app.static_folder = os.path.join(script_dir, 'assets')

# Configura o Flask para usar o caminho relativo ao diretório do script para os arquivos estáticos
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(script_dir, 'templates', 'view')),
    FileSystemLoader(os.path.join(script_dir, 'templates', 'components')),
])

# Carregar um modelo de NLP pré-treinado para análise de sentimento
nlp_model = pipeline('sentiment-analysis')

# Carregar dados do JSON do chatbot
with open(os.path.join(script_dir, 'chat_answers', 'dados_chatbot.json'), 'r', encoding='utf-8') as file:
    dados_chatbot = json.load(file)

# Carregar dados do JSON das vagas de emprego
with open(os.path.join(script_dir, 'chat_data', 'vagas_emprego.json'), 'r', encoding='utf-8') as file:
    dados_vagas = json.load(file)

# Carregar dados do JSON de cursos
with open(os.path.join(script_dir, 'chat_data', 'cursos.json'), 'r', encoding='utf-8') as file:
    dados_cursos = json.load(file)

# Carregar dados do JSON de notícias
with open(os.path.join(script_dir, 'chat_data', 'noticias.json'), 'r', encoding='utf-8') as file:
    dados_noticias = json.load(file)

# Extrair pares de respostas do JSON
pares = [(item['padrao'], item['respostas']) for item in dados_chatbot['pares']]

# Padrões relacionados a solicitação de notícias, cursos e empregos
padroes_noticias = dados_chatbot['padroes_noticias']
padroes_cursos = dados_chatbot['padroes_cursos']
padroes_empregos = dados_chatbot['padroes_empregos']

# Função para verificar se a mensagem contém um padrão relacionado a solicitação de notícias, cursos ou empregos
def verifica_solicitacao(mensagem, padroes):
    tokens = re.findall(r'\b\w+\b', mensagem.lower())  # Tokenização e conversão para minúsculas
    # Verificar se algum dos padrões está presente nos tokens
    for padrao in padroes:
        if padrao in tokens:
            return True
    return False

# Funções de pré-processamento de texto
def limpar_texto(texto):
    # Remover caracteres especiais e dígitos
    texto_limpo = re.sub(r'[^a-zA-Z\s]', '', texto)
    texto_limpo = re.sub(r'\d', '', texto_limpo)
    # Converter para minúsculas
    texto_limpo = texto_limpo.lower()
    return texto_limpo

def tokenizar_texto(texto):
    # Dividir o texto em palavras
    palavras = texto.split()
    return palavras

# Função para análise de sentimento usando o modelo pré-treinado
def analisar_sentimento(texto):
    resultado = nlp_model(texto)
    return resultado[0]['label']

# Função para processar a mensagem do usuário e retornar a resposta do chatbot
def chatbot(msg):
    for pattern, responses in pares:
        if re.match(pattern, msg, re.IGNORECASE):
            return random.choice(responses)

    if verifica_solicitacao(msg, padroes_noticias):
        resposta = "Claro! Aqui estão algumas notícias para você:<br><br>"
        for noticia in dados_noticias['noticias']:
            resposta += (
                f"<b>Título:</b> {noticia['titulo']}<br>"
                f"<b>Descrição:</b> {noticia['descricao']}<br>"
                f"<b>Fonte:</b> {noticia['fonte']}<br>"
                f"<b>Data:</b> {noticia['data']}<br>"
                "<br><hr><br>"
            )
        # Remove qualquer espaço extra no final
        return resposta.strip()

    elif verifica_solicitacao(msg, padroes_cursos):
        resposta = "Ótimo! Aqui estão alguns cursos que podem te interessar:<br><br>"
        for curso in dados_cursos['cursos']:
            resposta += (
                f"<b>Título:</b> {curso['titulo']}<br>"
                f"<b>Descrição:</b> {curso['descricao']}<br>"
                f"<b>Área de Atuação:</b> {curso['areaAtuacao']}<br>"
                f"<b>Preço:</b> {curso['preco']}<br>"
                f"<b>Duração:</b> {curso['duracao']}<br>"
                f"<a href='{curso['link']}' target='_blank'>Mais informações</a><br>"
                "<br><hr><br>"
            )
        # Remove qualquer espaço extra no final
        return resposta.strip()

    elif verifica_solicitacao(msg, padroes_empregos):
        resposta = "Legal! Aqui estão algumas vagas de emprego disponíveis:<br><br>"
        for vaga in dados_vagas['vagas']:
            resposta += (
                f"<b>Título:</b> {vaga['titulo']}<br>"
                f"<b>Descrição:</b> {vaga['descricao']}<br>"
                f"<b>Área de Atuação:</b> {vaga['areaAtuacao']}<br>"
                f"<b>Salário:</b> {vaga['salario']}<br>"
                f"<b>Requisitos:</b> {', '.join(vaga['requisitos'])}<br>"
                f"<b>Quantidade de Vagas:</b> {vaga['quantVagas']} Horário: {vaga['horas']}<br>"
                f"<b>CNPJ:</b> {vaga['cnpj']}<br>"
                "<br><hr><br>"
            )
        # Remove qualquer espaço extra no final
        return resposta.strip()

    elif "obrigado" in msg.lower():
        return "De nada! Estou aqui para ajudar."
    else:
        sentimento = analisar_sentimento(msg)
        if sentimento == 'NEGATIVE':
            respostas_negativas = [
                "Sinto muito que você esteja se sentindo assim. Posso te ajudar com algo?",
                "Fique tranquilo! Estou aqui para ajudar. Em que posso ser útil?",
                "Se precisar de ajuda, estou à disposição para conversar.",
                "Sinto muito que você esteja se sentindo assim. Como posso ajudar?",
                "Estou aqui para ajudar! O que você gostaria de fazer?",
            ]
            return random.choice(respostas_negativas)
        elif sentimento == 'POSITIVE':
            respostas_positivas = [
                "Ótimo ver que você está com um sentimento positivo! Em que posso ajudar?",
                "Que bom que você está se sentindo positivo hoje! Como posso ser útil?",
                "Fico feliz em saber que você está se sentindo bem! Em que posso te ajudar?",
                "Que ótimo que você está se sentindo assim! Como posso ajudar?",
                "Estou feliz em ver que você está com um sentimento positivo! O que você gostaria de fazer?",
            ]
            return random.choice(respostas_positivas)
        else:
            return "Interessante! Em que mais posso ajudar?"

# Rota para o chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot_endpoint():
    user_input = request.json["msg"]
    response = chatbot(user_input)
    return jsonify({"response": response})

# Rota para buscar vagas, cursos e notícias por área de atuação
@app.route("/areasearch")
def buscar():
    # Obter a área ou áreas a partir dos parâmetros da URL
    areas = request.args.get('area', default='', type=str).split(',')

    vagas_encontradas = []
    cursos_encontrados = []
    noticias_encontradas = []

    # Carregar dados do JSON das vagas de emprego
    with open(os.path.join(script_dir, 'chat_data', 'vagas_emprego.json'), 'r', encoding='utf-8') as file:
        dados_vagas = json.load(file)

    # Carregar dados do JSON de cursos
    with open(os.path.join(script_dir, 'chat_data', 'cursos.json'), 'r', encoding='utf-8') as file:
        dados_cursos = json.load(file)

    # Carregar dados do JSON de notícias
    with open(os.path.join(script_dir, 'chat_data', 'noticias.json'), 'r', encoding='utf-8') as file:
        dados_noticias = json.load(file)

    # Buscar vagas de emprego por área de atuação
    for vaga in dados_vagas['vagas']:
        for area in areas:
            if area.strip().lower() in vaga['areaAtuacao'].lower():
                vagas_encontradas.append(vaga)
                break  # Parar de verificar outras áreas se a vaga foi encontrada

    # Buscar cursos por área de atuação
    for curso in dados_cursos['cursos']:
        for area in areas:
            if area.strip().lower() in curso['areaAtuacao'].lower():
                cursos_encontrados.append(curso)
                break  # Parar de verificar outras áreas se o curso foi encontrado

    # Buscar notícias por área de atuação
    for noticia in dados_noticias['noticias']:
        for area in areas:
            if area.strip().lower() in noticia['areaAtuacao'].lower():
                noticias_encontradas.append(noticia)
                break  # Parar de verificar outras áreas se a notícia foi encontrada

    return jsonify({
        "vagas": vagas_encontradas,
        "cursos": cursos_encontrados,
        "noticias": noticias_encontradas
    })

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
