
from flask import g, make_response, redirect, url_for
from functions.db_treco import apagar_usuario

def mod_apagausuario(mysql):
    # Apaga um usuário do sistema
    # Também apaga todos os seus "trecos"

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    apagar_usuario(mysql, g)

    # Página de destino de logout
    resposta = make_response(redirect(url_for('login')))

    # apaga o cookie do usuário
    resposta.set_cookie(
        key='usuario',  # Nome do cookie
        value='',  # Apara o valor do cookie
        max_age=0  # A validade do cookie é ZERO
    )

    # Redireciona para login
    return resposta