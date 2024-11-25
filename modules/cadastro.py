
from flask import g, redirect, render_template, request, url_for
from functions.db_treco import cadastra_usuario


def mod_cadastro(mysql):

    jatem = ''
    success = False

    # Se o usuário está logado redireciona para a página de perfil
    if g.usuario != '':
        return redirect(url_for('perfil'))

    if request.method == 'POST':

        form = dict(request.form)

        cadastra_usuario(mysql, form)

        success = True

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Cadastre-se',
        'jatem': jatem,
        'success': success,
    }

    return render_template('cadastro.html', **pagina)