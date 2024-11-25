
from flask import g, render_template


def mod_erro():

    pagina = {
    'titulo': 'CRUDTrecos - Erro 404',
    'usuario': g.usuario,
    }
    return render_template('404.html', **pagina), 404
