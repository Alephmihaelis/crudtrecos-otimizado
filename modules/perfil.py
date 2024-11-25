
from flask import g, redirect, render_template, url_for
from functions.geral import calcular_idade


def mod_perfil(mysql):

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    # Calcula idade do usuário
    g.usuario['idade'] = calcular_idade(g.usuario['nascimento'])

    # Obtém a quantidade de trecos ativos do usuário
    sql = "SELECT count(t_id) AS total FROM treco WHERE t_usuario = %s AND t_status = 'on'"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    # Teste de mesa
    # print('\n\n\n DB', row, '\n\n\n')

    # Adiciona a quantidade ao perfil
    g.usuario['total'] = row['total']

    # Dados, variáveis e valores a serem passados para o template HTML
    pagina = {
        'titulo': 'CRUDTrecos - Novo Treco',
        'usuario': g.usuario,
    }

    # Renderiza o template HTML, passaod valores para ele
    return render_template('perfil.html', **pagina)