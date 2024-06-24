from flask import redirect, url_for, session, render_template, flash, request
from ldap3 import Server, Connection, ALL
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações LDAP
LDAP_SERVER = os.getenv('SERVER')
LDAP_USER_DN = os.getenv('USER_DN')
LDAP_USER_PASSWORD = os.getenv('USER_PASSWORD')
LDAP_BASE_DN = os.getenv('BASE_DN')

def ldap_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Conectar ao servidor LDAP com o usuário de ligação
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, user=LDAP_USER_DN, password=LDAP_USER_PASSWORD, auto_bind=True)

        # Pesquisar o DN completo do usuário
        search_filter = f'(sAMAccountName={username})'
        conn.search(search_base=LDAP_BASE_DN, search_filter=search_filter, attributes=['distinguishedName'])

        if not conn.entries:
            flash('Credenciais inválidas', 'error')
            return redirect(url_for('login'))

        user_dn = conn.entries[0].distinguishedName.value

        # Autenticar o usuário com o DN completo e a senha fornecida
        user_conn = Connection(server, user=user_dn, password=password)

        if user_conn.bind():
            session['user'] = username
            return redirect(url_for('protected'))
        else:
            flash('Credenciais inválidas', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

def protected():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('protected.html', username=session['user'])

def logout():
    session.pop('user', None)
    return redirect(url_for('login'))
