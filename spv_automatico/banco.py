# Módulo: banco.py (responsável por interação com o banco de dados)

import psycopg2

DB_CONFIG = {
    'host': '191.252.191.49',
    'user': 'fidelity',
    'password': 'fidelity123',
    'database': 'db_fidelity',
    'port': '5432'
}

def conectar():
    return psycopg2.connect(**DB_CONFIG)

def buscar_pesquisas(filtro):
    con = conectar()
    cursor = con.cursor()
    cond = ''
    if filtro in (1, 3):
        cond = ' AND rg <> "" '

    sql = f'''
    SELECT DISTINCT p.Cod_Cliente, p.Cod_Pesquisa,  e.UF, p.Data_Entrada,
           coalesce(p.nome_corrigido, p.nome) AS Nome, p.CPF,
           coalesce(p.rg_corrigido, p.rg) AS RG, p.Nascimento,
           coalesce(p.mae_corrigido, p.mae) AS Mae, p.anexo AS Anexo,
           ps.Resultado, ps.cod_spv_tipo
    FROM pesquisa p
         INNER JOIN servico s ON p.Cod_Servico = s.Cod_Servico
         LEFT JOIN lote_pesquisa lp ON p.Cod_Pesquisa = lp.Cod_Pesquisa
         LEFT JOIN lote l ON l.cod_lote = lp.cod_lote
         LEFT JOIN estado e ON e.Cod_UF = p.Cod_UF
         LEFT JOIN pesquisa_spv ps ON ps.Cod_Pesquisa = p.Cod_Pesquisa AND ps.Cod_SPV = 1 AND ps.filtro = {filtro}
    WHERE p.Data_Conclusao IS NULL AND ps.resultado IS NULL AND p.tipo = 0
          AND (({filtro} = 0 AND coalesce(p.cpf, '') <> '') 
           OR  ({filtro} IN (1,3) AND coalesce(p.RG, '') <> '')
           OR  ({filtro} = 2 AND coalesce(p.nome_corrigido, p.nome, '') <> ''))
          AND (e.UF = 'SP' OR p.Cod_UF_Nascimento = 26 OR p.Cod_UF_RG = 26)
    -- GROUP BY p.cod_pesquisa
    ORDER BY nome ASC, resultado DESC
    LIMIT 210
    '''

    cursor.execute(sql)
    dados = cursor.fetchall()
    cursor.close()
    return dados

def salvar_resultado(codPesquisa, resultado, filtro):
    sql = f'''
    INSERT INTO pesquisa_spv (
        Cod_Pesquisa, Cod_SPV, Cod_spv_computador,
        Cod_Spv_Tipo, Resultado, Cod_Funcionario, filtro, website_id
    ) VALUES (
        {codPesquisa}, 1, 36, NULL, {resultado}, -1, {filtro}, 1
    )
    ON CONFLICT (cod_pesquisa) 
    DO UPDATE SET
        Cod_SPV = EXCLUDED.Cod_SPV,
        Cod_spv_computador = EXCLUDED.Cod_spv_computador,
        Cod_spv_tipo = EXCLUDED.Cod_spv_tipo,
        Resultado = EXCLUDED.Resultado,
        Cod_Funcionario = EXCLUDED.Cod_Funcionario,
        filtro = EXCLUDED.filtro,
        website_id = EXCLUDED.website_id
    '''
    con = conectar()
    cursor = con.cursor()
    cursor.execute(sql)
    con.commit()
    cursor.close()
