
from flask import g, redirect, url_for

from functions.db_treco import apaga_tudo

def mod_apaga(id, mysql):
    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    apaga_tudo(mysql, id)

    # Retorna para a lista de items
    return redirect(url_for('index', a='apagado'))
