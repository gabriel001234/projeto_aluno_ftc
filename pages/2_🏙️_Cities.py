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
st.set_page_config(page_title='Visão Cidades', page_icon=img_path, layout='wide')

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

st.title('🏙️ Visão Cidades')
st.write('')

# Top 10 cidades com mais restaurantes
top_10_most_restaurants = df.loc[:, ['restaurant_id', 'country', 'city']].groupby(['country', 'city']).count().reset_index().sort_values(['restaurant_id', 'city'], ascending=[False, True]).head(10)

st.plotly_chart(create_bar_graph(top_10_most_restaurants, True, {'x': {'city': 'Cidades'}, 'y': {'restaurant_id': 'Quantidade de restaurantes'}}, 'Top 10 cidades com mais restaurantes', 'country'), use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    # Top 7 cidades com restaurantes com média de avaliação acima de 4
    top_7_best_ratings = df.loc[df['aggregate_rating'] >= 4, ['restaurant_id', 'country', 'city']].groupby(['country', 'city']).count().reset_index().sort_values(['restaurant_id', 'city'], ascending=[False, True]).head(7)
    
    st.plotly_chart(create_bar_graph(top_7_best_ratings, True, {'x': {'city': 'Cidades'}, 'y': {'restaurant_id': 'Quantidade de restaurantes'}}, 'Top 7 cidades com restaurantes com média de avaliação acima de 4', 'country'), use_container_width=True)
    
with col2:
    # Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5
    top_7_worst_ratings = df.loc[df['aggregate_rating'] <= 2.5, ['restaurant_id', 'country', 'city']].groupby(['country', 'city']).count().reset_index().sort_values(['restaurant_id', 'country'], ascending=[False, True]).head(7)
    
    st.plotly_chart(create_bar_graph(top_7_worst_ratings, True, {'x': {'city': 'Cidades'}, 'y': {'restaurant_id': 'Quantidade de restaurantes'}}, 'Top 7 cidades com restaurantes com média de avaliação abaixo de 2.5', 'country'), use_container_width=True)

# Top 10 cidades com tipos culinários distintos
top_10_most_culinaries = df.loc[:, ['cuisines', 'country', 'city']].groupby(['country', 'city']).nunique().reset_index().sort_values(['cuisines', 'city'], ascending=[False, True]).head(10)

st.plotly_chart(create_bar_graph(top_10_most_culinaries, True, {'x': {'city': 'Cidades'}, 'y': {'cuisines': 'Quantidade de tipos culinários'}}, 'Top 10 cidades com tipos culinários distintos', 'country'), use_container_width=True)

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