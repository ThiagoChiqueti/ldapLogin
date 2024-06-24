from flask import Flask
from flask_session import Session
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'  # Sessão temporária armazenada no sistema de arquivos
app.config['SESSION_PERMANENT'] = False  # Sessão não persistente

Session(app)

# Rotas e lógica de autenticação
from auth import ldap_login, protected, logout

app.add_url_rule('/', 'login', ldap_login, methods=['GET', 'POST'])
app.add_url_rule('/protected', 'protected', protected)
app.add_url_rule('/logout', 'logout', logout)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
