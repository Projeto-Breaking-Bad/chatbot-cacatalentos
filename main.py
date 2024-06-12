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
]

# Criação do chatbot
def chatbot(msg):
    for pattern, responses in pares:
        if msg.lower() == pattern.lower():
            return responses[0]

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