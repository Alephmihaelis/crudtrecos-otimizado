

from flask import abort, g, redirect, render_template, request, url_for


def mod_edita(id, mysql):

    # Se o usuário não está logado redireciona para a página de login
    if g.usuario == '':
        return redirect(url_for('login'))

    # Se o formulário foi enviado
    if request.method == 'POST':
        form = dict(request.form)

        # print('\n\n\n FORM:', form, '\n\n\n')

        sql = '''
            UPDATE treco 
            SET t_foto = %s,
                t_nome = %s,
                t_descricao = %s,
                t_localizacao = %s
            WHERE t_id = %s
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (
            form['foto'],
            form['nome'],
            form['descricao'],
            form['localizacao'],
            id,
        ))
        mysql.connection.commit()
        cur.close()

        # Após editar, retorna para a lista de itens
        return redirect(url_for('index', a='editado'))

    sql = '''
        SELECT * FROM treco
        WHERE t_id = %s
            AND t_usuario = %s
            AND t_status = 'on'
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (id, g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    # print('\n\n\n DB:', row, '\n\n\n')

    if row == None:
        abort(404)

    pagina = {
        'titulo': 'CRUDTrecos',
        'usuario': g.usuario,
        'item': row,
    }

    return render_template('edita.html', **pagina)
