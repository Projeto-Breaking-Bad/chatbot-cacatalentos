import os
import random
import re
from flask import Flask, render_template, request, jsonify
from jinja2 import ChoiceLoader, FileSystemLoader
from transformers import pipeline  # Importar a biblioteca transformers para análise de sentimento

app = Flask(__name__)

# Obtém o caminho do diretório do script atual
script_dir = os.path.dirname(os.path.abspath(__file__))

# Configura o Flask para usar o caminho relativo ao diretório do script para templates
app.template_folder = os.path.join(script_dir, 'templates')

# Configura o Flask para usar o caminho relativo ao diretório do script para os arquivos estáticos
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(script_dir, 'templates', 'view')),
    FileSystemLoader(os.path.join(script_dir, 'templates', 'components')),
])

# Carregar um modelo de NLP pré-treinado para análise de sentimento
nlp_model = pipeline('sentiment-analysis')

# Pares de respostas para o chatbot
pares = [
    (
        r"Oi|Olá|Ei",
        ["Olá! Como posso ajudar você?", "Oi! Em que posso te ajudar?"]
    ),
    (
        r"quero encontrar vagas de emprego",
        ["Ótimo! Qual área você está procurando?", "Claro! Em qual área você está interessado?"]
    ),
    (
        r"quero ver notícias",
        ["Certamente! De qual área você gostaria de ver notícias?", "Claro! Qual área você está interessado em ver notícias?"]
    ),
    (
        r"quero encontrar cursos",
        ["Legal! Qual área você quer estudar?", "Ótimo! Em qual área você quer encontrar cursos?"]
    ),
    (
        r"sair|tchau|até logo",
        ["Até mais! Se precisar de mais alguma coisa, estarei por aqui.", "Tchau! Tenha um bom dia."]
    ),
    (
        r"python|java|javascript|php",
        ["Ótimo! Essas são ótimas escolhas. Existem muitas oportunidades nessas áreas!", "Essas linguagens de programação são muito populares no mercado atualmente."]
    ),
    (
        r"desenvolvedor|programador",
        ["Ser um desenvolvedor é uma ótima escolha de carreira! Existem muitas oportunidades para programadores atualmente."]
    ),
    (
        r"engenharia de software|ciência da computação",
        ["Essas são excelentes áreas para estudar! Existem muitas oportunidades de carreira em engenharia de software e ciência da computação."]
    ),
    (
        r"tecnologia da informação|TI",
        ["TI é uma área em constante crescimento! Existem muitas oportunidades de carreira em tecnologia da informação."]
    ),
]

# Padrões relacionados a solicitação de notícias, cursos e empregos
padroes_noticias = ["notícias", "últimas notícias", "novidades", "atualizações"]
padroes_cursos = ["cursos", "aprender", "estudar", "formação", "capacitação"]
padroes_empregos = ["emprego", "vagas", "trabalho", "oportunidades"]

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
        return "Claro! Aqui estão algumas notícias para você..."
    elif verifica_solicitacao(msg, padroes_cursos):
        return "Ótimo! Aqui estão alguns cursos que podem te interessar..."
    elif verifica_solicitacao(msg, padroes_empregos):
        return "Legal! Aqui estão algumas vagas de emprego disponíveis..."
    else:
        sentimento = analisar_sentimento(msg)
        if sentimento == 'NEGATIVE':
            return "Parece que você está com um sentimento negativo. Como posso ajudar?"
        elif sentimento == 'POSITIVE':
            return "Ótimo ver que você está com um sentimento positivo! Em que posso ajudar?"
        else:
            return "Interessante! Em que mais posso ajudar?"

# Rota para o chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot_endpoint():
    user_input = request.json["msg"]
    response = chatbot(user_input)
    return jsonify({"response": response})

# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.static_folder = os.path.join(script_dir, 'assets')
    app.run(debug=True)
