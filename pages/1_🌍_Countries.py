# Import
import pandas         as pd
import streamlit      as st
import plotly.express as px

@st.cache_data
def load_data(path):
    """ Esta função tem a responsabilidade de fazer a carga de dados e salvar em um dataframe

        Input: path (str)
        Output: DataFrame
    """    
    return pd.read_csv(path)

def create_sidebar(df):
    """ Esta função tem a responsabilidade de criar a barra lateral

        Input: df (DataFrame)
        Output: list
    """ 
    
    with st.sidebar:
        with st.container():
            col1, col2 = st.columns([5, 20])
    
            with col1:
                st.image(img_path, width=45)
            with col2:
                st.write('# Fome Zero')
                
        with st.container():
            st.write('')
            st.write('### Filtros')
    
            countries = df['country'].unique().tolist()
            countries.sort()
            country_select = st.multiselect('Escolha de quais países deseja visualizar os restaurantes', countries, countries)

    return country_select

def create_bar_graph(df, auto, labels, title, color=None):
    """ Esta função tem a responsabilidade de criar um gráfico de barras

        Input: df (DataFrame), auto (bool ou str), labels (dict), title (str), color (str - opcional)
        Output: Figure
    """
    
    title_layout = {
        'text': title,
        'y': 1,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'   
}
    
    x = list(labels['x'].keys())[0]
    y = list(labels['y'].keys())[0] 

    labels['x'].update(labels['y'])
    labels.pop('y')
    
    bar = px.bar(df, x=x, y=y, text=y, text_auto=auto, labels=labels['x'], color=color)
    bar.update_layout(title=title_layout)

    return bar

path = 'datasets/clean/zomato.csv'
img_path = 'img/logo.png'

# Definindo configuração da página
st.set_page_config(page_title='Visão Países', page_icon=img_path, layout='wide')

# Carregamento dos dados limpos
df = load_data(path)

# ------------------------------- Início da lógica do programa

# -------------------------------
# Barra Lateral
# -------------------------------

country_select = create_sidebar(df)
df=df[df['country'].isin(country_select)]

# ---------------------------------------------
# Layout no Streamlit
# ---------------------------------------------

st.title('🌍 Visão Países')
st.write('')

# Quantidade de restaurantes por país
restaurants_by_country = df.loc[:, ['restaurant_id', 'country']].groupby('country').count().reset_index().sort_values('restaurant_id', ascending=False)

st.plotly_chart(create_bar_graph(restaurants_by_country, True, {'x': {'country': 'Países'}, 'y': {'restaurant_id': 'Quantidade de restaurantes'}}, 'Quantidade de restaurantes registrados por país'), use_container_width=True)

st.write('---')

# Quantidade de cidades por país
cities_by_country = df.loc[:, ['city', 'country']].groupby('country').nunique().reset_index().sort_values('city', ascending=False)

st.plotly_chart(create_bar_graph(cities_by_country, True, {'x': {'country': 'Países'}, 'y': {'city': 'Quantidade de cidades'}}, 'Quantidade de cidades registradas por país'), use_container_width=True)

st.write('---')

col1, col2 = st.columns(2)

with col1:
    # Média de avaliações feitas por país
    votes_by_country = df.loc[:, ['votes', 'country']].groupby('country').mean().reset_index().sort_values('votes', ascending=False)

    st.plotly_chart(create_bar_graph(votes_by_country, '.2f', {'x': {'country': 'Países'}, 'y': {'votes': 'Quantidade de avaliações'}}, 'Média de avaliações feitas por país'), use_container_width=True)
    
with col2:
    # Média de preço de um prato para duas pessoas por país
    average_cost_for_two_by_country = df.loc[:, ['average_cost_for_two', 'country']].groupby('country').mean().reset_index().sort_values('average_cost_for_two', ascending=False)

    st.plotly_chart(create_bar_graph(average_cost_for_two_by_country, '.2f', {'x': {'country': 'Países'}, 'y': {'average_cost_for_two': 'Preço de prato para duas pessoas'}}, 'Média de preço de um prato para duas pessoas por país'), use_container_width=True)

# ---------------------------------------------
# Alterando texto padrão do multiselect
# ---------------------------------------------
multi_css="""
<style>
.stMultiSelect div div div div div:nth-of-type(2) {visibility: hidden;}
.stMultiSelect div div div div div:nth-of-type(2)::before {visibility: visible; content: 'Escolha uma opção';}
</style>
"""
st.markdown(multi_css, unsafe_allow_html=True)