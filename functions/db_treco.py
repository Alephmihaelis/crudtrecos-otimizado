
from flask import g

from functions.geral import gerar_senha

def get_all_trecos(mysql):
    # Obtém todos os 'trecos' do usuário conectado
    sql = '''
        SELECT t_id, t_foto, t_nome, t_descricao, t_localizacao
        FROM treco
        WHERE t_usuario = %s
            AND t_status = 'on'
        ORDER BY t_data DESC
    '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    rows = cur.fetchall()
    cur.close()

    return rows

def get_active_trecos(mysql):
    # Obtém a quantidade de trecos ativos do usuário
    sql = "SELECT count(t_id) AS total FROM treco WHERE t_usuario = %s AND t_status = 'on'"
    cur = mysql.connection.cursor()
    cur.execute(sql, (g.usuario['id'],))
    row = cur.fetchone()
    cur.close()

    return row

def apaga_tudo(mysql, id):
    # (des)comente o método para apagar conforme o seu caso
    # Apaga completamente o treco (CUIDADO!)
    # sql = 'DELETE FROM treco WHERE t_id = %s'
    # Altera o status do treco para 'del' (Mais seguro)
    sql = "UPDATE treco SET t_status = 'del'  WHERE t_id = %s"

    # Executa o SQL
    cur = mysql.connection.cursor()
    cur.execute(sql, (id,))
    mysql.connection.commit()
    cur.close()

def novo_treco(mysql, form):
        
        # Grava os dados no banco de dados
        sql = '''
            INSERT INTO treco (
                t_usuario, t_foto, t_nome, t_descricao, t_localizacao
            ) VALUES (
                %s, %s, %s, %s, %s
            )
        '''
        cur = mysql.connection.cursor()
        cur.execute(sql, (
            g.usuario['id'],
            form['foto'],
            form['nome'],
            form['descricao'],
            form['localizacao'],
        ))
        mysql.connection.commit()
        cur.close()

def nova_senha(mysql, form):

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

def fazer_login(mysql, form):
    
    sql = '''
        SELECT *,
        -- Gera uma versão das datas em pt-BR para salvar no cookie
        DATE_FORMAT(u_data, '%%d/%%m/%%Y às %%H:%%m') AS u_databr,
        DATE_FORMAT(u_nascimento, '%%d/%%m/%%Y') AS u_nascimentobr
        FROM usuario
        WHERE u_email = %s
            AND u_senha = SHA1(%s)
            AND u_status = 'on'
        '''
    cur = mysql.connection.cursor()
    cur.execute(sql, (form['email'], form['senha'],))
    usuario = cur.fetchone()
    cur.close()

    return usuario
