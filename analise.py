import pandas as pd

uf_dict = {
    11: "Rondônia",
    12: "Acre",
    13: "Amazonas",
    14: "Roraima",
    15: "Pará",
    16: "Amapá",
    17: "Tocantins",
    21: "Maranhão",
    22: "Piauí",
    23: "Ceará",
    24: "Rio Grande do Norte",
    25: "Paraíba",
    26: "Pernambuco",
    27: "Alagoas",
    28: "Sergipe",
    29: "Bahia",
    31: "Minas Gerais",
    32: "Espírito Santo",
    33: "Rio de Janeiro",
    35: "São Paulo",
    41: "Paraná",
    42: "Santa Catarina",
    43: "Rio Grande do Sul",
    50: "Mato Grosso do Sul",
    51: "Mato Grosso",
    52: "Goiás",
    53: "Distrito Federal"
}

uf_regiao_dict_id = {
    11: "Norte",
    12: "Norte",
    13: "Norte",
    14: "Norte",
    15: "Norte",
    16: "Norte",
    17: "Norte",
    21: "Nordeste",
    22: "Nordeste",
    23: "Nordeste",
    24: "Nordeste",
    25: "Nordeste",
    26: "Nordeste",
    27: "Nordeste",
    28: "Nordeste",
    29: "Nordeste",
    31: "Sudeste",
    32: "Sudeste",
    33: "Sudeste",
    35: "Sudeste",
    41: "Sul",
    42: "Sul",
    43: "Sul",
    50: "Centro-Oeste",
    51: "Centro-Oeste",
    52: "Centro-Oeste",
    53: "Centro-Oeste"
}


uf_regiao_dict_sigla = {
    'AC': 'Norte',
    'AL': 'Nordeste',
    'AP': 'Norte',
    'AM': 'Norte',
    'BA': 'Nordeste',
    'CE': 'Nordeste',
    'DF': 'Centro-Oeste',
    'ES': 'Sudeste',
    'GO': 'Centro-Oeste',
    'MA': 'Nordeste',
    'MT': 'Centro-Oeste',
    'MS': 'Centro-Oeste',
    'MG': 'Sudeste',
    'PA': 'Norte',
    'PB': 'Nordeste',
    'PR': 'Sul',
    'PE': 'Nordeste',
    'PI': 'Nordeste',
    'RJ': 'Sudeste',
    'RN': 'Nordeste',
    'RS': 'Sul',
    'RO': 'Norte',
    'RR': 'Norte',
    'SC': 'Sul',
    'SP': 'Sudeste',
    'SE': 'Nordeste',
    'TO': 'Norte'
}
sexo_dict = {
    1: "Homem",
    2: "Mulher"
}


cor_raca_dict = {
    1: "Branca",
    2: "Preta",
    3: "Amarela",
    4: "Parda",
    5: "Indígena",
    9: "Ignorado"
}
sintomas_dict = {
    1: "Sim",
    2: "Não",
    3: "Não sabe",
    9: "Ignorado"
}
teste_coronavirus_dict = {
    1: "Positivo",
    2: "Negativo",
    3: "Inconclusivo",
    4: "Ainda não recebeu o resultado",
    9: "Ignorado",
		None: None
}
fez_isolamento_dict = {
    1: "Não fez restrição, levou vida normal como antes da pandemia",
    2: "Reduziu o contato com as pessoas, mas continuou saindo de casa para trabalho ou atividades não essenciais e/ou recebendo visitas",
    3: "Ficou em casa e só saiu em caso de necessidade básica",
    4: "Ficou rigorosamente em casa",
    9: "Ignorado"
}

fez_isolamento_dict_v2 = {
    1: "Não",
    2: "Moderado",
    3: "Sim",
    4: "Totalmente",
    9: "Ignorado"
}
procurou_unid_saude_dict = {
    1: "Sim",
    2: "Não",
    9: "Ignorado",
    None: None
}
recebeu_aux_dict = {
    1: "Sim",
    2: "Não"
}
faixa_rendimento_dict = {
    0: '0 - 100',
    1: '101 - 300',
    2: '301 - 600',
    3: '601 - 800',
    4: '801 - 1.600',
    5: '1.601 - 3.000',
    6: '3.001 - 10.000',
    7: '10.001 - 50.000',
    8: '50.001 - 100.000',
    9: '+100.000'
}

def gravidade_caso(row):
    gravidade = ''
    if row['sin_febre'] == "Sim" or row['sin_tosse'] == "Sim" or row['sin_dor_garganta'] == "Sim" or row['sin_dor_cabeca'] == "Sim" or row['sin_nausea'] == "Sim" or row['sin_nariz_entup'] == "Sim"or row['sin_fadiga'] == "Sim" or row['sin_perda_olf'] == "Sim" or row['sin_dor_muscular'] == "Sim":
        gravidade = 'Leve'
        
    if row['sin_dific_respirar'] == "Sim" or row['si_dor_peito'] == "Sim":
        gravidade = 'Grave'

    if gravidade == '':
        gravidade = 'Assintomático'
    return gravidade

def tratamento_df(df_trabalho):
    colunas_sintomas = df_trabalho.iloc[:, 4:-5]
    lista_colunas_sintomas = colunas_sintomas.columns.to_list()

    df_trabalho.uf = df_trabalho.uf.map(uf_dict)
    df_trabalho.sexo = df_trabalho.sexo.map(sexo_dict)
    df_trabalho.cor_raca = df_trabalho.cor_raca.map(cor_raca_dict)
    df_trabalho.resultado_teste = df_trabalho.resultado_teste.map(teste_coronavirus_dict)
    df_trabalho.fez_isolamento = df_trabalho.fez_isolamento.map(fez_isolamento_dict_v2)
    df_trabalho.procurou_unid_saude = df_trabalho.procurou_unid_saude.map(procurou_unid_saude_dict)
    df_trabalho.recebeu_aux = df_trabalho.recebeu_aux.map(recebeu_aux_dict)
    df_trabalho.faixa_rendimento = df_trabalho.faixa_rendimento.map(faixa_rendimento_dict)

    for coll in lista_colunas_sintomas:
        df_trabalho[coll] = df_trabalho[coll].map(sintomas_dict)

    return df_trabalho