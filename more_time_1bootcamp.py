
# =====================
# Essa seria a versão com mais 1 hora disponível.
# =====================

import pandas as pd
import streamlit as st
import folium
import plotly.express as px
from streamlit_folium import folium_static
import plotly.graph_objects as go

df = pd.read_csv('ab_raw.csv' )
df1 = df.copy()
st.set_page_config( layout='wide')

# ===================================================================
# Slidebar no streamlit 
# =================================================================== 

st.header('BootCamp #1 - Airbnb') 


# Comando pra trazer imagem
image = st.sidebar.image( 'icon.png', width=120)


st.sidebar.markdown('# Airbnb Company')
st.sidebar.markdown("""---""")  

st.sidebar.markdown('## Price Filter') 

price_slider = st.sidebar.slider(
    'Select a price:',
    1.0, 10000.0, (10000.0))


st.sidebar.markdown("""---""")

st.sidebar.markdown('## Cities')
region_options = st.sidebar.multiselect(
    'Select the Region', 
    ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'], 
    default=['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'] ) 


st.sidebar.markdown("""---""") 
st.sidebar.markdown("### Powered by Comunidade DS.")
st.sidebar.markdown("###### Talitha Oliveira, Gabriel Azevedo")


# Select filter default
price_sel = df1['price'] <= price_slider
df1 = df1.loc[price_sel, :]

region_sel = df1['neighbourhood_group'].isin( region_options ) 
df1 = df1.loc[region_sel, :]

# ===================================================================
#                     Layout no streamlit 
# ===================================================================

tab1, tab2 = st.tabs( ['Visão Geral', 'Mapas'] )


with tab1: 
    
    
    with st.container(): 
            col1, col2, col3 = st.columns(3)
            
            with col1:
            
                st.markdown('#### Valor médio do aluguel em NY')

                rent_mean = round(df1['price'].mean(), 2)
                st.metric(' ', rent_mean)



            with col2:
                st.markdown('#### Aluguel diário mais caro em NY')

                rent_max = round(df1['price'].max(), 2)
                st.metric(' ',rent_max)



            with col3:    
                st.markdown('##### Variação dos preços dos imóveis em NY')   

                rent_std = round(df1['price'].std(),2)
                st.metric(' ',rent_std)

    st.markdown("""---""")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('#### Média da diária de cada região')

        fig1 = mean_price_data = df1[['neighbourhood_group', 'price']].groupby('neighbourhood_group').mean().sort_values('price', ascending=False).reset_index()

        fig1 = px.bar(fig1, x='neighbourhood_group', y = 'price', text_auto=True)
        fig1.update_xaxes(title_text='Região')
        fig1.update_yaxes(title_text='Preço')

        st.plotly_chart( fig1, use_container_width=True)


    with col2: 
        st.markdown('#### Média da diária por tipo de acomodação')
        
        fig2 = mean_price_data = df1[['room_type', 'price']].groupby('room_type').mean().sort_values('price', ascending=False).reset_index()
        
        fig2 = px.pie(fig2, names='room_type', values='price')

        st.plotly_chart( fig2, use_container_width=True)


         
with tab2:         


    col1, col2 = st.columns(2)
    
    with col1: 
        st.markdown('#### Top 10 imóveis com mais avaliações, por região')
        
        df1['color'] = 'NA'

        df1.loc[df1['neighbourhood_group'] == 'Bronx', 'color'] = 'darkgreen'
        df1.loc[df1['neighbourhood_group'] == 'Manhattan', 'color'] = 'darkred'
        df1.loc[df1['neighbourhood_group'] == 'Queens', 'color'] = 'purple'
        df1.loc[df1['neighbourhood_group'] == 'Staten Island', 'color'] = 'beige'
        df1.loc[df1['neighbourhood_group'] == 'Brooklyn', 'color'] = 'cadetblue'

        cols = ['id', 'neighbourhood_group', 'latitude', 'longitude', 'number_of_reviews', 'color']

        region_top10_review = df1.loc[:, cols].sort_values('number_of_reviews', ascending=False).groupby('neighbourhood_group').head(10).reset_index(drop=True)

        region_top10_review = region_top10_review.sort_values(['neighbourhood_group', 'number_of_reviews'], ascending=[True, False]).reset_index(drop=True)

        map = folium.Map(location = [40.712776, -74.005974], zoom_start=11)

        for i, c in region_top10_review.iterrows():
            folium.Marker(  [c['latitude'], c['longitude']],
                            popup=c['neighbourhood_group'],
                            icon=folium.Icon(color = c['color'])).add_to(map)
        folium_static(map)

        
    with col2: 
        st.markdown('#### Top 50 maiores preços')
        cols = ['neighbourhood_group', 'latitude', 'longitude', 'price', 'color']
        top50_high_price = df1.loc[:, cols].sort_values('price', ascending=False).head(50).reset_index(drop=True)
        top50_high_price = top50_high_price.sort_values('price', ascending=False)

        map = folium.Map(location = [40.712776, -74.005974], zoom_start=11)

        for i, c in top50_high_price.iterrows():
            folium.Marker(  [c['latitude'], c['longitude']],
                            popup=c['price'],
                            icon=folium.Icon(color = c['color'])).add_to(map)

        folium_static(map )
        
        
        
    with st.container(): 

        st.markdown('#### Top 10 menores preços')    
        cols = ['id', 'neighbourhood_group', 'latitude', 'longitude', 'price', 'color']

        region_bottom10_price = df1.loc[df1['price'] > 0, cols].sort_values(['neighbourhood_group', 'price'], ascending = True).groupby('neighbourhood_group').head(10).reset_index(drop=True)

        map = folium.Map(location = [40.712776, -74.005974], zoom_start=11)

        for i, c in region_bottom10_price.iterrows():
            folium.Marker(  [c['latitude'], c['longitude']],
                            popup=c['neighbourhood_group'],
                            icon=folium.Icon(color = c['color'])).add_to(map)

        folium_static(map)
    
    

    

        
        
    
        
        

    





