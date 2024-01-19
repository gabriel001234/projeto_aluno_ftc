# Imports
import folium
import pandas    as pd
import streamlit as st

from streamlit_folium import folium_static
from folium.plugins   import MarkerCluster

@st.cache_data
def load_data(path):
    """ Esta função tem a responsabilidade de fazer a carga de dados e salvar em um dataframe

        Input: path (str)
        Output: DataFrame
    """ 
    
    return pd.read_csv(path)

def to_csv(df):
    """ Esta função tem a responsabilidade de converter um dataframe para .CSV e retornar os bytes do arquivo

        Input: path (str)
        Output: bytes
    """     
    return df.to_csv(index=False).encode('utf-8')

def create_sidebar(df):
    """ Esta função tem a responsabilidade de criar a barra lateral

        Input: df (DataFrame)
        Output: multiselect
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
    

def create_map(df):
    location = (df['latitude'].mean(), df['longitude'].mean())
    map = folium.Map(location, zoom_start=2, control_scale=True)
    cluster = MarkerCluster().add_to(map)

    for _, row in df.iterrows():
        
        html = f"""
        <p>
            <strong>{row['restaurant_name']}</strong>
        </p>
        <p>
            Price: {row['average_cost_for_two']},00 ({row['currency']}) para dois</br>
            Type: {row['cuisines']}</br>
            Aggregate Rating: {row['aggregate_rating']}/5.0
        </p>    
        """
        
        folium.Marker((row['latitude'], row['longitude']), popup=folium.Popup(html, max_width=500), icon=folium.Icon(icon='house', prefix='fa', color=row['rating_color_name'])).add_to(cluster)

    return map
    
path = 'datasets/clean/zomato.csv'
img_path = 'img/logo.png'

# Definindo configuração da página
st.set_page_config(page_title='Home', page_icon=img_path, layout='wide')

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

st.title('Fome Zero!')
st.header('O Melhor lugar para encontrar seu mais novo restaurante favorito!')
st.subheader('Temos as seguintes marcas dentro da nossa plataforma:')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric('Restaurantes cadastrados', df['restaurant_id'].shape[0])

    with col2:
        st.metric('Países cadastrados', df['country'].nunique())

    with col3:
        st.metric('Cidades cadastradas', df['city'].nunique())

    with col4:
        st.metric('Avaliações feitas na plataforma', f'{df["votes"].sum():,}'.replace(',', '.'))

    with col5:
        st.metric('Tipos de culinária oferecidos', df['cuisines'].nunique())

folium_static(create_map(df), width=1060, height=450)

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
