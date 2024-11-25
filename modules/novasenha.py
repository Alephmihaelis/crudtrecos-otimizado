
from flask import g, redirect, render_template, request, url_for
from functions.db_treco import nova_senha
from functions.geral import gerar_senha


def mod_novasenha(mysql):

    novasenha = ''
    erro = False

    # Se o usuário está logado, redireciona para a página de perfil
    if g.usuario != '':
        return redirect(url_for('perfil'))

    # Se o formulário foi enviado
    if request.method == 'POST':

        # Obtém dados preenchidos
        form = dict(request.form)

        # Teste de mesa
        # print('\n\n\n FORM:', form, '\n\n\n')

        nova_senha(mysql, form)

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Nova Senha',
        'erro': erro,
        'novasenha': novasenha,
    }

    return render_template('novasenha.html', **pagina)