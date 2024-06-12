import random
import re
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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
        return "Desculpe, não entendi o que você disse."

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
    app.run(debug=True)
