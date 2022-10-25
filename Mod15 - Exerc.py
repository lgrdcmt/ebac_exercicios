import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import streamlit as st
import time

sns.set()


def plota_pivot_table(df, value, index, func, ylabel, xlabel, opcao = 'nada', titulo = 'nada'):
    if opcao == 'nada':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).plot(figsize=[15, 5])
    elif opcao == 'unstack':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).unstack().plot(figsize=[15, 5])
    elif opcao == 'sort':
        pd.pivot_table(df, values=value, index=index,aggfunc=func).sort_values(value).plot(figsize=[15, 5])
    plt.title(titulo)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    st.pyplot(fig = plt)
    return None


listas =  [
    ['IDADEMAE', 'DTNASC', 'mean', 'média idade mãe por data', 'data nascimento', 'nada' , 'media idade mae por data'],
    ['IDADEMAE', ['DTNASC', 'SEXO'], 'mean', 'media idade mae','data de nascimento','unstack', 'media idade mae por sexo'],
    ['PESO', ['DTNASC', 'SEXO'], 'mean', 'media peso bebe','data de nascimento','unstack', 'media peso bebe por sexo'],
    ['PESO', 'ESCMAE', 'median', 'PESO mediano','escolaridade mae','sort', 'mediano por escolaridade mae'],
    ['APGAR1', 'GESTACAO', 'mean', 'apgar1 medio','gestacao','sort', 'media apgar1 por gestacao']
          ]


st.set_page_config(page_title = 'SINASC Rondônia - 2019', 
                   page_icon = 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Bandeira_de_Rond%C3%B4nia.svg',
                   layout = 'wide')

st.write('# Análise SINASC Rondônia - 2019')

DATA_URL = './Mod14/input/SINASC_RO_2019.csv'

@st.cache(allow_output_mutation = True)

def load_data():
    data = pd.read_csv(DATA_URL)
    time.sleep(2)
    return data



data_load_state = st.text('Loading data...')

sinasc = load_data()

data_load_state.text('Loading data... done!')

data_load_state.empty()

st.balloons()

sinasc['DTNASC'] = pd.to_datetime(sinasc['DTNASC'])

sinasc['DTNASC_MES'] = (sinasc.DTNASC.dt.strftime('%m')).astype(int)

min_data = sinasc['DTNASC'].min()
max_data = sinasc['DTNASC'].max()

st.sidebar.write('#### Opções de Visualizações')

name = st.sidebar.text_input('Entre com o seu nome: ').upper()


escolha = st.sidebar.radio(
    "Deseja escolher por mês ou data inicial e final:",
    ('Data Inicial e Data Final', 'Mês')
    )


if escolha == 'Mês':
    mes = st.sidebar.slider('Mês', 1, 12, 1)
    
    sinascfilter = sinasc[sinasc['DTNASC_MES'] == mes]
    
    data_inicial = sinascfilter['DTNASC'].dt.strftime('%Y-%m-%d').min()
    data_final = sinascfilter['DTNASC'].dt.strftime('%Y-%m-%d').max()

else:

    data_inicial = st.sidebar.date_input('Data Inicial',
                value = min_data,
                min_value = min_data,
                max_value = max_data)

    data_final = st.sidebar.date_input('Data Final',
                value = max_data,
                min_value = min_data,
                max_value = max_data)

data_inicial_exibicao = (pd.to_datetime(data_inicial)).strftime('%d/%m/%Y')
data_final_exibicao = (pd.to_datetime(data_final)).strftime('%d/%m/%Y')

st.write(f'Seja muito bem vindo(a) {name}, abaixo seguem os gráficos com os parâmetros selecionados na barra lateral.')
st.write('Para imprimir ou gerar PDF, fechar a barra lateral e apertar CTRL + P')

st.markdown(f'''
<table style="width:100%">
  <tr>
    <th>DATA INICIAL</th>
    <th>DATA FINAL</th>
  </tr>
  <tr>
    <td>{data_inicial_exibicao}</td>
    <td>{data_final_exibicao}</td>
  </tr>
</table>
</br>
''', unsafe_allow_html=True)

teste = sinasc[(sinasc['DTNASC'] <= pd.to_datetime(data_final)) & (sinasc['DTNASC'] >= pd.to_datetime(data_inicial))]

if st.sidebar.checkbox('Ver Dados Brutos'):
    st.subheader('Dados Brutos')
    st.write(sinasc)

if st.sidebar.checkbox('Ver Dados Filtrados'):
    st.subheader('Dados Filtrados')
    st.write(teste)

st.sidebar.write('Quantidade de Linhas')
st.sidebar.write('Filtrado = ', teste.shape[0])
st.sidebar.write('Total = ', sinasc.shape[0])

for lista in listas:
    plota_pivot_table(teste, lista[0], lista[1], lista[2], lista[3], lista[4], lista[5], lista[6])