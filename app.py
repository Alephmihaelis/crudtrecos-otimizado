# Importa as dependências do aplicativo
from flask import Flask, abort, g, make_response, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import json
from functions.geral import calcular_idade, datetime_para_string, gerar_senha, remove_prefixo
from modules.apaga import mod_apaga
from modules.apagausuario import mod_apagausuario
from modules.cadastro import mod_cadastro
from modules.edita import mod_edita
from modules.editaperfil import mod_editaperfil
from modules.index import mod_index
from modules.login import mod_login
from modules.logout import mod_logout
from modules.novasenha import mod_novasenha
from modules.novo import mod_novo
from modules.perfil import mod_perfil

# Cria um aplicativo Flask chamado "app"
app = Flask(__name__)

# Configurações de acesso ao MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudtrecos'

# Setup da conexão com MySQL
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['MYSQL_USE_UNICODE'] = True
app.config['MYSQL_CHARSET'] = 'utf8mb4'

# Variável de conexão com o MySQL
mysql = MySQL(app)


@app.before_request
def start():

    # Setup do MySQL para corrigir acentuação
    cur = mysql.connection.cursor()
    cur.execute("SET NAMES utf8mb4")
    cur.execute("SET character_set_connection=utf8mb4")
    cur.execute("SET character_set_client=utf8mb4")
    cur.execute("SET character_set_results=utf8mb4")

    # Setup do MySQL para dias da semana e meses em português
    cur.execute("SET lc_time_names = 'pt_BR'")

    # Lê o cookie do usuário → 'usuario'
    cookie = request.cookies.get('usuario')

    if cookie:
        # Se o cookie existe, Converte o valor dele de JSON para dicionário
        g.usuario = json.loads(cookie)
    else:
        # Se o cookie não existe, a variável do usuário está vazia
        g.usuario = ''


@app.route("/")  # Rota raiz, equivalente à página inicial do site (index)
def index():  # Função executada ao acessar a rota raiz
    return mod_index(mysql=mysql)


# Rota para a página de cadastro de novo treco
@app.route('/novo', methods=['GET', 'POST'])
def novo():  # Função executada para cadastrar novo treco
    return mod_novo(mysql=mysql)


@app.route('/edita/<id>', methods=['GET', 'POST'])
def edita(id):
    return mod_edita(id, mysql=mysql)


@app.route('/apaga/<id>')
def apaga(id):
    return mod_apaga(id, mysql=mysql)

@app.route('/login', methods=['GET', 'POST'])  # Rota para login de usuário
def login():
    return mod_login(mysql=mysql)


@app.route('/logout')
def logout():
    return mod_logout()


@app.route('/cadastro', methods=['GET', 'POST'])  # Cadastro de usuário
def cadastro():
    return mod_cadastro(mysql=mysql)


@app.route('/novasenha', methods=['GET', 'POST'])  # Pedido de senha de usuário
def novasenha():
    return mod_novasenha(mysql=mysql)

@app.route('/perfil')
def perfil():
    return mod_perfil(mysql=mysql)

@app.route('/apagausuario')
def apagausuario():
    return mod_apagausuario(mysql=mysql)

@app.route('/editaperfil', methods=['GET', 'POST'])
def editaperfil():
    return mod_editaperfil(mysql=mysql)

@app.errorhandler(404)
def page_not_found(e):
    pagina = {
        'titulo': 'CRUDTrecos - Erro 404',
        'usuario': g.usuario,
    }
    return render_template('404.html', **pagina), 404


# Executa o servidor HTTP se estiver no modo de desenvolvimento
# Remova / comente essas linhas no modo de produção
if __name__ == '__main__':
    app.run(debug=True)
