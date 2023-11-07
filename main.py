import streamlit as st
import pandas as pd
import analise as an
from dados import dados_pesquisa
import altair as alt
import plotly.express as px

PRIMARY_COLOR = "#572b52"

def apply_custom_style():
    st_custom_style = """
                <style>
                summary {
                    display: none;
                }
                h2 {
                    color: {prim-color};
                }
                header[data-testid="stHeader"] {
                    background-image: linear-gradient({prim-color}, {prim-color}, purple);
                }
                div[data-testid="stStatusWidget"] div div div svg{
                    color: white;
                }
                #relat-rio-de-exporta-o-de-vinhos, #tabela-resumida-com-informa-es-de-exporta-es-nos-ltimos-anos{
                    text-align:center;
                }
                div[data-testid="stStatusWidget"] img{
                    opacity: 100%;
                }
                div[data-testid="stStatusWidget"] label{
                    color: white;
                }
                div[data-testid="stStatusWidget"] button{
                    color: white;
                    background: #9e829b;
                    border-radius: 20px;
                }
                #MainMenu{
                    color: white;
                    visibility: hidden;
                }
                * {
                  -webkit-user-drag: none;
                  -khtml-user-drag: none;
                  -moz-user-drag: none;
                  -o-user-drag: none;
                  user-drag: none;
                }
                a[href="#hide"] {
                    visibility: hidden;
                }
                div[data-testid="stDecoration"] {
                    background-image: none;
                    background-color: black;
                }
                section>div.block-container {
                    padding-top: 60px;
                }
                thead tr th:first-child {
                    display:none
                }
                tbody th {
                    display:none
                }
                .stAlert a {
                    display: none;
                }
                button[role="tab"][aria-selected="true"] {
                    background: #9e829b;
                    padding: 4px;
                    border-top-left-radius: 10px;
                    border-top-right-radius: 10px;
                    color: white;
                }
                div[data-testid="collapsedControl"] {
                    color: white;
                }
                [tabindex="0"] > * {
                
                    max-width: 86rem !important;
                }
                #grupo {
                    background: #9e829b;
                    padding: 15px;
                    border-radius: 10px;
                }
                </style>
                """.replace('{prim-color}', PRIMARY_COLOR)
    st.markdown(st_custom_style, unsafe_allow_html=True)

if __name__== '__main__':
    apply_custom_style()

    col_1, col_principal, col_2 = st.columns(3)

    with col_principal:
        st.image('assets/ibge.png')

        st.header('Mapeamento da Covid')
        st.subheader('Dados sobre covid IBGE')

    st.write('Com base na análise dos dados emitidos da pesquisa do IBGE \
             PNAD-COVID-19, foram gerados insights sobre algumas caracteristicas \
             sobre os dados da população, clinicos, comportamento  e econômico.')

    st.markdown('Referência da <a href=\
                "https://www.ibge.gov.br/estatisticas/investigacoes-experimentais/estatisticas-experimentais/27946-divulgacao-semanal-pnadcovid1?t=downloads&utm_source=covid19&utm_medium=hotsite&utm_campaign=covid_19\
                ">pesquisa<a/>.', unsafe_allow_html=True)

    st.write('Os dados que foram levados em conta para montar o relatório são os seguintes')

    st.dataframe(pd.read_csv('./datasets_gerados/Dados_PNAD_utilizados.csv', encoding='utf-8'))

    st.markdown('<hr/>', unsafe_allow_html=True)

    tab_tratamento, tab_analise, tab_conclusao = st.tabs(['Tratamento dados', 'Análise', 'Propostas de ações'])

    with tab_tratamento:
        st.subheader('Iniciativa BigQuery')

        st.write('Nesta pesquisa realizada pelo IBGE, há uma quantidade relativamente alta para o trabalho completo com, \
                 todos os dados, por este motivo, com o intuito de acelerar o processamento e auxiliar a pesquisa, foi \
                 foi utilizado uma primeira fase de seleção e tratamento, usando conceitos de SQL query para extrair \
                 as informações de forma limpa e consolidada')

        st.write('Abaixo são informados os indicativos de seleção da base usando a linguagem SQL: ')

        st.write('1. Importação bases')
        st.write('Na pesquisa foram utilizados dados de 3 periodos que estavam separados em um periodo por arquivo. \
                 Cada base foi adicionada no projeto - notional-grove-399523')
        
        with st.expander('Importação'):
            st.image('./assets/prints/importacao_base.png')

        st.write('Na exploração inicial, foi selecionando todos os dados até 1000 linhas e entendo sua organização e tipos')
        st.code('''
            SELECT * FROM 
    `notional-grove-399523.base_dados_pnad_covid.base-09-2020` --Nome da tabela gerada pela consolidação das bases
LIMIT 1000
        ''')
        with st.expander('Consulta'):
            st.image('./assets/prints/consulta_limit.png')
            st.image('./assets/prints/consulta_limit_detalhes.png')


        st.write('2. Tratamento inicial já com os dados da selecionados e com nomeclatura já definida')
        st.code('''
            SELECT UF as uf,
       A002 as idade,
       A003 as sexo,
       A004 as cor_raca,
       B0011 as sin_febre,
       B0012 as sin_tosse,
       B0013 as sin_dor_garganta,
       B0014 as sin_dific_respirar,
       B0015 as sin_dor_cabeca,
       B0016 as si_dor_peito,
       B0017 as sin_nausea,
       B0018 as sin_nariz_entup,
       B0019 as sin_fadiga,
       B00111 as sin_perda_olf,
       B00112 as sin_dor_muscular,
       B008 as fez_teste,
       B011 as fez_isolamento,
       B002 as procurou_unid_saude,
       D0051 as recebeu_aux,
       C011A11 as faixa_rendimento,
FROM `notional-grove-399523.base_dados_pnad_covid.base-09-2020`
LIMIT 1000
''')
        with st.expander('Filtro'):
            st.image('./assets/prints/consulta_filtrado_limit.png')

        st.write('3. Para a junção das bases - usada a instrução UNION ALL - que agrega os resultados vindos de um select')
        st.code("""
        SELECT UF as uf,
       A002 as idade,
       A003 as sexo,
       A004 as cor_raca,
       B0011 as sin_febre,
       B0012 as sin_tosse,
       B0013 as sin_dor_garganta,
       B0014 as sin_dific_respirar,
       B0015 as sin_dor_cabeca,
       B0016 as si_dor_peito,
       B0017 as sin_nausea,
       B0018 as sin_nariz_entup,
       B0019 as sin_fadiga,
       B00111 as sin_perda_olf,
       B00112 as sin_dor_muscular,
       B008 as fez_teste,
       B011 as fez_isolamento,
       B002 as procurou_unid_saude,
       D0051 as recebeu_aux,
       C011A11 as faixa_rendimento,
FROM `notional-grove-399523.base_dados_pnad_covid.base-09-2020` -- Primeira base
                UNION ALL
SELECT UF as uf,
       A002 as idade,
       A003 as sexo,
       A004 as cor_raca,
       B0011 as sin_febre,
       B0012 as sin_tosse,
       B0013 as sin_dor_garganta,
       B0014 as sin_dific_respirar,
       B0015 as sin_dor_cabeca,
       B0016 as si_dor_peito,
       B0017 as sin_nausea,
       B0018 as sin_nariz_entup,
       B0019 as sin_fadiga,
       B00111 as sin_perda_olf,
       B00112 as sin_dor_muscular,
       B008 as fez_teste,
       B011 as fez_isolamento,
       B002 as procurou_unid_saude,
       D0051 as recebeu_aux,
       C011A11 as faixa_rendimento,
FROM `notional-grove-399523.base_dados_pnad_covid.base-10-2020` -- Segunda base
                UNION ALL
SELECT UF as uf,
       A002 as idade,
       A003 as sexo,
       A004 as cor_raca,
       B0011 as sin_febre,
       B0012 as sin_tosse,
       B0013 as sin_dor_garganta,
       B0014 as sin_dific_respirar,
       B0015 as sin_dor_cabeca,
       B0016 as si_dor_peito,
       B0017 as sin_nausea,
       B0018 as sin_nariz_entup,
       B0019 as sin_fadiga,
       B00111 as sin_perda_olf,
       B00112 as sin_dor_muscular,
       B008 as fez_teste,
       B011 as fez_isolamento,
       B002 as procurou_unid_saude,
       D0051 as recebeu_aux,
       C011A11 as faixa_rendimento,
FROM `notional-grove-399523.base_dados_pnad_covid.base-11-2020` -- Terceira base
""")
        with st.expander('Consolidação'):
            st.image('./assets/prints/union_1.png')
            st.image('./assets/prints/union_2.png')

            st.write('Conversão da query para tabela')

            st.image('./assets/prints/union_3.png')
            st.image('./assets/prints/union_4.png')
            st.image('./assets/prints/union_5.png')

        st.write('4. Integração via colab')
        st.write('Por meio do colab é feita a conexão com o ambiente do BigQuery, desta forma \
                 com o notebook pode ser feita chamadas SQL diretamente pelo colab')
        
        with st.expander('Colab'):
            st.image('./assets/prints/integracao_1.png')
            st.image('./assets/prints/integracao_2.png')
            st.image('./assets/prints/integracao_3.png')
            st.image('./assets/prints/integracao_4.png')

    with tab_analise:
        # Distribuição
        with st.container():
            st.subheader('Distribuição da pesquisa')

            # Gráfico da pesquisa
            dataset_uf = pd.read_csv('./datasets_gerados/dataset_uf_pesquisa.csv')

            # KPI dos entrevistados em cada mês
            dataset_uf = dataset_uf.rename(columns={'mes': 'Qtde entrevistados'})

            st.write('O levantamento feito pelo IBGE, elaborou as questões nos 26 estados e \
                        distrito federal, sendo os 3 maiores pesquisados - Minas Gerais, São Paulo e \
                        Rio de Janeiro.')
            st.bar_chart(dataset_uf, x='UF', y='Qtde entrevistados')

            st.write('A pesquisa teve duração de 3 meses no ano de 2020, com base no gráfico se percebe \
                    qual mês houve a progressão do volume de respostas')
            
            dataset_mes = pd.read_csv('./datasets_gerados/mes_group.csv')
            for i,r in dataset_mes.iterrows():
                st.metric(f'{r["mes"]}', r['Qtd Entrevistados'])
            #st.bar_chart(dataset_mes, x='mes', y='Qtd Entrevistados')
    
            df_trabalho = pd.read_csv('./datasets_gerados/tabela-tratada-result-test-09-a-11-2020.csv') # OK

        with st.container():
            st.subheader('Caracteristicas da população')

            st.write('1.1 - Distribuição de entrevistados por imagem')
            scatter = alt.Chart(df_trabalho).mark_bar(width=15).encode(
                alt.X("idade", bin=True, scale=alt.Scale(bins=[df_trabalho.idade.min(),
                                                                df_trabalho.idade.min() + 20,
                                                                df_trabalho.idade.min() + 40,
                                                                df_trabalho.idade.min() + 60,
                                                                df_trabalho.idade.min() + 80])),
                y='count()',
            )
            st.altair_chart(scatter)

            st.write('1.2 - Composição do sexo nos entrevistados')
            df = px.data.tips()
            s_sexo = df_trabalho['sexo'].value_counts(normalize=True).round(4)*100 #proporção sexo pesquisa total
            lbl_sexo = ['Mulher', 'Homem']
            fig = px.pie(values=s_sexo, names=lbl_sexo, color=['red', 'blue'])
            print(s_sexo.index)
            st.plotly_chart(fig)

        with st.container():
           

            st.subheader('Avaliação das respostas não respondidas dos entrevistados')
            percent_nulos = 100*((df_trabalho.isnull().sum())/(len(df_trabalho))).round(3) # avaliação de dados nulos
            percent_nulos = percent_nulos.sort_values(ascending=True)
            df_percent_nulos = pd.DataFrame(percent_nulos, columns=['Qtde Valores Nulos'])

            st.bar_chart(df_percent_nulos, y='Qtde Valores Nulos')

            st.write("""
                Com exceção aos dados relacionados ao usuário (uf, idade, sexo e cor_raça),
                todos os demais dados contém dados nulos ou ausentes, com uma maior concentração nas colunas:

                *   "resultado_teste" - `96% de dados ausentes`
                *   "procurou_unid_saude" - `96% de dados ausentes`
                *   "faixa_rendimento" - `63% de dados ausentes`


                Em específico, a coluna "resultado_teste" chama a atenção pelo volume de dados faltantes.
                Este fato deverá ser levado em consideração em relação às análises realizadas nesse documento,
                principalmente em relação às de espécie clínica e econômicas.
            """)

            st.subheader('Análise de famílias positivadas a partir do teste de covid')

            st.write("""
                Ao todo, `14.450` famílias receberam um diagnóstico positivo em relação ao teste de Covid.

                > `28,4%` da população que fez teste de Covid

                > `1,3%` da população total da base.

                > Apenas `4%` da população realizaram um teste para diagnóstico (50.931).
            """)
        
            df_fez_teste = df_trabalho["resultado_teste"].count()
            df_positivados = df_trabalho[df_trabalho["resultado_teste"] == "Positivo"]
            share_positivados_total = ((len(df_positivados))/(len(df_trabalho))) * 100
            share_positivados_test = ((len(df_positivados))/ df_fez_teste) * 100
            share_fizeram_teste = (df_fez_teste /(len(df_trabalho))) * 100

            st.write("Total de famílias que fizeram teste: {:,.0f}".format(df_fez_teste))
            st.write("Total de famílias positivadas: {:,.0f}".format(len(df_positivados)))
            st.write("Share de famílias que fizeram teste: {:.1f}%".format(share_fizeram_teste))
            st.write("Share Positivados versus fizeram teste: {:.1f}%".format(share_positivados_test))
            st.write("Share Positivados versus total da base: {:.1f}%".format(share_positivados_total))

            st.write('---')

            st.subheader("Relação entre familias positivadas versus famílias sintomáticas ( 2 ou + sintomas)")
            st.write("""
                > Com o baixo volume de testes e de famílias positivadas, buscamos entender se haveria um volume maior de famílias sintómáticas. Ou seja, que apresentaram 2 ou mais sintomas.

                Famílias sintomáticas:
                *   `2.1%` em relação ao total da base total
                *   `48%` das famílias sintomáticas fizeram o teste de Covid
                *   `59%` das famílias positivadas apresentaram mais de 2 sintomas
            """)

            colunas_sintomas = df_trabalho.iloc[:, 4:-5]
            lista_colunas_sintomas = colunas_sintomas.columns.to_list() # criação de uma lista contendo nomes de columas de sintomas
            
            sintomas_dict = {
                1: "Sim",
                2: "Não",
                3: "Não sabe",
                9: None
            }

            for coll in lista_colunas_sintomas:
                df_trabalho[coll] = df_trabalho[coll].map(sintomas_dict)

            # Tratamento e adição de uma nova coluna no dataframe com a soma de sintomas por família (qtd_sintomas)
            tem_sint = {"Sim" : True, "Não" : False,"Não sabe" : False,None : False}
            df_sintomas = df_trabalho.iloc[:, 4:-6]

            for coll in df_sintomas.columns.to_list():
                df_sintomas[coll] = df_sintomas[coll].map(tem_sint)

            qtd_sintomas = df_sintomas.sum(axis=1)
            df_trabalho['qtd_sintomas'] = qtd_sintomas
            
            nome_colunas_sintomas = df_sintomas.columns.to_list() # listagem de colunas com sintomas
            total_sin_por_coluna = df_trabalho[nome_colunas_sintomas].apply(lambda col: (col == 'Sim').sum()).sort_values(ascending=False) # Contabilize o total de "Sim" em cada coluna de sintomas

            total_sin_por_coluna.name = 'Volume de familias com sintomas'
            st.bar_chart(total_sin_por_coluna)