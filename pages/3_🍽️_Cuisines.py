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
        Output: tuple
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

            st.write('---')       

            restaurants = st.slider('Selecione a quantidade de restaurantes que deseja visualizar', min_value=1, max_value=20, value=10)

            st.write('---')

            cuisines = df['cuisines'].unique().tolist()
            cuisines.sort()
            cuisine_select = st.multiselect('Escolha de quais países deseja visualizar os restaurantes', cuisines, ['American', 'Arabian', 'BBQ', 'Brazilian', 'Home-made', 'Italian', 'Japanese'])         

    return country_select, restaurants, cuisine_select

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

def metrics(df):
    """ Esta função tem a responsabilidade de mostrar as métricas dos melhores restraurantes por tipo de culinária

        Input: df (DataFrame)
        Output: None
    """  
    
    italian, american, arabian, japonese, brazilian = st.columns(5)
    
    with italian:
        best_italian = df.loc[df['cuisines'] == 'Italian', :]
        
        if len(best_italian) == 0:
            st.metric('Italiana: NaN', value='nan')
            
        else:
            best_italian = best_italian.iloc[0, :]
            st.metric(label=f'Italiana: {best_italian["restaurant_name"]}', value=f'{best_italian["aggregate_rating"]}/5.0', help=f"""
            País: {best_italian["country"]}\n
            Cidade: {best_italian["city"]}\n
            Média prato para dois: {best_italian["average_cost_for_two"]} ({best_italian["currency"]})
        """)
    
    with american:
        best_american = df.loc[df['cuisines'] == 'American', :]

        if len(best_american) == 0:
            st.metric('Americana: NaN', value='nan')
        
        else:
            best_american = best_american.iloc[0, :]
            st.metric(label=f'Americana: {best_american["restaurant_name"]}', value=f'{best_american["aggregate_rating"]}/5.0', help=f"""
            País: {best_american["country"]}\n
            Cidade: {best_american["city"]}\n
            Média prato para dois: {best_american["average_cost_for_two"]} ({best_american["currency"]})
        """)
        
    with arabian:
        best_arabian = df.loc[df['cuisines'] == 'Arabian', :]

        if len(best_arabian) == 0:
            st.metric('Árabe: NaN', value='nan')

        else:  
            best_arabian = best_arabian.iloc[0, :]
            st.metric(label=f'Árabe: {best_arabian["restaurant_name"]}', value=f'{best_arabian["aggregate_rating"]}/5.0', help = f"""
            País: {best_arabian["country"]}\n
            Cidade: {best_arabian["city"]}\n
            Média prato para dois: {best_arabian["average_cost_for_two"]} ({best_arabian["currency"]})
        """)
        
    with japonese:
        best_japanese = df.loc[df['cuisines'] == 'Japanese', :]

        if len(best_japanese) == 0:
            st.metric('Japonesa: NaN', value='nan')

        else:
            best_japanese = best_japanese.iloc[0, :]
            st.metric(label=f'Japonesa: {best_japanese["restaurant_name"]}', value=f'{best_japanese["aggregate_rating"]}/5.0', help = f"""
            País: {best_japanese["country"]}\n
            Cidade: {best_japanese["city"]}\n
            Média prato para dois: {best_japanese["average_cost_for_two"]} ({best_japanese["currency"]})
        """)
        
    with brazilian:
        best_brazilian = df.loc[df['cuisines'] == 'Brazilian', :]

        if len(best_brazilian) == 0:
            st.metric('Brasileira: NaN', value='nan')

        else:
            best_brazilian = best_brazilian.iloc[0, :]
            st.metric(label=f'Brasileira: {best_brazilian["restaurant_name"]}', value=f'{best_brazilian["aggregate_rating"]}/5.0', help = f"""
            País: {best_brazilian["country"]}\n
            Cidade: {best_brazilian["city"]}\n
            Média prato para dois: {best_brazilian["average_cost_for_two"]} ({best_brazilian["currency"]})
        """)

    return None

path = 'datasets/clean/zomato.csv'
img_path = 'img/logo.png'

# Definindo configuração da página
st.set_page_config(page_title='Visão Tipos Culinários', page_icon=img_path, layout='wide')

# Carregamento dos dados limpos
df = load_data(path)

# ------------------------------- Início da lógica do programa

# -------------------------------
# Barra Lateral
# -------------------------------

country_select, restaurants, cuisine_select = create_sidebar(df)

df = df.loc[(df['country'].isin(country_select)), ['restaurant_id', 'restaurant_name', 'country', 'city', 'cuisines', 'average_cost_for_two', 'currency', 'aggregate_rating', 'votes']].sort_values(['aggregate_rating', 'restaurant_id'], ascending=[False, True])

# ---------------------------------------------
# Layout no Streamlit
# ---------------------------------------------
# ---------------------------------------------

st.title('🍽️ Visão Tipos Culinários')
st.write('')

# Melhores restaurantes dos principais tipos culinários
st.header('Melhores restaurantes dos principais tipos culinários')

metrics(df)

# Top restaurantes
st.header(f'Top {restaurants} Restaurantes')

st.dataframe(df.loc[(df['cuisines'].isin(cuisine_select))].head(restaurants), column_config={'restaurant_id': st.column_config.NumberColumn(format="%d"), 'average_cost_for_two': st.column_config.NumberColumn(format="%d"), 'aggregate_rating': st.column_config.NumberColumn(format="%.4f"), 'votes': st.column_config.NumberColumn(format="%d")})

st.write('---')

best, worst = st.columns(2)

with best:
    # Melhores Tipos de Culinária
    top_best_cuisines = df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=False).reset_index().head(10)

    st.plotly_chart(create_bar_graph(top_best_cuisines, True, {'x': {'cuisines': 'Tipo de culinária'}, 'y': {'aggregate_rating': 'Avaliação média'}}, 'Melhores Tipos de Culinária (todos)'), use_container_width=True)

with worst:
    # Piores Tipos de Culinária
    top_worst_cuisines = df.loc[:, ['aggregate_rating', 'cuisines']].groupby('cuisines').mean().sort_values('aggregate_rating', ascending=True).reset_index().head(10)

    st.plotly_chart(create_bar_graph(top_worst_cuisines, True, {'x': {'cuisines': 'Tipo de culinária'}, 'y': {'aggregate_rating': 'Avaliação média'}}, 'Piores Tipos de Culinária (todos)'), use_container_width=True)

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