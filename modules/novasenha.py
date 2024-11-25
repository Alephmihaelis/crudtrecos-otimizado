
from flask import g, redirect, render_template, request, url_for

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

        # Pesquisa pelo email e nascimento informados, no banco de dados
        sql = '''
            SELECT u_id
            FROM usuario
            WHERE u_email = %s
                AND u_nascimento = %s
                AND u_status = 'on'
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (form['email'], form['nascimento'],))
        row = cur.fetchone()
        cur.close()

        # Teste de mesa
        # print('\n\n\n DB:', row, '\n\n\n')

        # Se o usuário não existe
        if row == None:
            # Exibe mensagem no frontend
            erro = True
        else:
            # Gera uma nova senha
            novasenha = gerar_senha()

            # Salva a nova senha no banco de dados
            sql = "UPDATE usuario SET u_senha = SHA1(%s) WHERE u_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(sql, (novasenha, row['u_id'],))
            mysql.connection.commit()
            cur.close()

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Nova Senha',
        'erro': erro,
        'novasenha': novasenha,
    }

    return render_template('novasenha.html', **pagina)