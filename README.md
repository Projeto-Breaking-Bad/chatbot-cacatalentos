# Caça Talentos - Chatbot para Busca de Empregos e Recursos Profissionais

## Descrição
O Caça Talentos é um chatbot desenvolvido em Python para ajudar estudantes e profissionais a encontrar vagas de emprego, acessar notícias relacionadas às áreas de trabalho e descobrir cursos e locais para aprimorar suas habilidades profissionais. O chatbot é uma ferramenta interativa e amigável que utiliza processamento de linguagem natural para compreender e responder às perguntas dos usuários.

## Funcionalidades
- Responder a cumprimentos e iniciar conversas.
- Auxiliar na busca por vagas de emprego, recomendando cursos e notícias relevantes.
- Oferecer informações sobre cursos e locais para estudar áreas específicas de trabalho.
- Fornecer uma experiência de chatbot intuitiva e fácil de usar.

## Dependências
- Flask: Um framework web leve para Python utilizado para criar o servidor que hospeda o chatbot.
- pip install Flask
- NLTK (Natural Language Toolkit): Uma biblioteca Python popular para processamento de linguagem natural, usada para criar o chatbot e compreender as perguntas dos usuários.
- pip install nltk
- pip install Jinja2
- pip install transformers
- pip install gunicorn

# Instalar todas essas dependências
- pip install -r requirements.txt

## Endpoints

- "/chatbot": http://127.0.0.1:5000/
- "/areasearch": http://127.0.0.1:5000/areasearch?area=TI,%20Telecomunica%C3%A7%C3%B5es

## Docker Compose

- docker-compose up --build

## Docker

- docker build -t chatbotcacatalentos .
- docker run -p 5000:5000 chatbotcacatalentos