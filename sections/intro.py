import streamlit as st
import plotly.express as px
from urllib.request import urlopen
import json
import pandas as pd

def show(df):
    st.title("Digital Cultural Consumption in France")  
    st.markdown("""
### Why This Matters
In a world where screens shape cultural habits, understanding how **French audiences engage with digital culture** 
reveals both **economic trends** and **social inequalities** in access, spending, and digital awareness.
""")

    st.markdown("""
    ## As streaming platforms multiply, French consumers are redefining how they access and value culture online.
    
    This dashboard uncovers **who consumes, how, and why**, revealing the patterns that shape modern digital culture.
    """)

        # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Respondents", len(df))

    # --- Sécuriser la moyenne d'âge ---
    try:
        avg_age = pd.to_numeric(df['age'], errors='coerce').mean()
        col2.metric("Average Age", f"{int(avg_age)}" if pd.notna(avg_age) else "N/A")
    except Exception as e:
        col2.metric("Average Age", "N/A")
        st.warning(f"Erreur lors du calcul de l'âge : {e}")

    # --- Autres métriques ---
    try:
        avg_spend = round(df['depense_mensuelle_culturelle'].mean(skipna=True), 2)
    except Exception:
        avg_spend = "N/A"
    col3.metric("Avg. Monthly Spend (€)", avg_spend)

    try:
        mode_freq = df['frequence_internet'].mode().iloc[0]
    except Exception:
        mode_freq = "N/A"
    col4.metric("Internet Frequency Mode", mode_freq)


    st.markdown("---")

    region_counts = df['region'].value_counts().reset_index()
    region_counts.columns = ['region', 'count']

    with urlopen("https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/regions.geojson") as response:
        france_geojson = json.load(response)

    region_counts['region'] = region_counts['region'].str.replace("’", "'", regex=False)

    fig_map = px.choropleth(
        region_counts,
        geojson=france_geojson,
        locations='region',
        featureidkey="properties.nom",
        color='count',
        color_continuous_scale="Blues",
        title="Regional Distribution of Respondents in France",
        hover_data=['count']
    )

    fig_map.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        showcountries=False,
        showcoastlines=True,
        coastlinecolor="gray"
    )

    fig_map.update_layout(
        width=900,
        height=600,
        margin={"r":0,"t":40,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        coloraxis_colorbar=dict(title="Respondents", tickvals=[0, 250, 500, 750, 1000])
    )

    st.plotly_chart(fig_map, use_container_width=True, key="intro_map")

    st.info(""" 
Respondents are concentrated in major urban and coastal regions notably Île-de-France and Provence-Alpes-Côte d’Azur.  
This distribution mirrors national population patterns and access to digital infrastructure.
""")

    st.markdown("---")
    # ================================
    # SECOND MAP — Average Spending by Region (€)
    # ================================

    spending_region = (df.groupby('region', as_index=False)['depense_mensuelle_culturelle'].mean().rename(columns={'depense_mensuelle_culturelle': 'avg_spending'}))

    spending_region['region'] = spending_region['region'].str.replace("’", "'", regex=False)

    fig_spend_map = px.choropleth(
        spending_region,
        geojson=france_geojson,
        locations='region',
        featureidkey="properties.nom",
        color='avg_spending',
        color_continuous_scale="YlGnBu",
        title="Average Monthly Cultural Spending (€) by Region",
        hover_data={'avg_spending': ':.2f'}
    )

    fig_spend_map.update_geos(
        fitbounds="locations",
        visible=False,
        projection_type="mercator",
        showcountries=False,
        showcoastlines=True,
        coastlinecolor="gray"
    )

    fig_spend_map.update_layout(
        width=900,
        height=600,
        margin={"r":0,"t":40,"l":0,"b":0},
        geo=dict(bgcolor='rgba(0,0,0,0)'),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        coloraxis_colorbar=dict(title="€ / month", tickprefix="€")
    )

    st.plotly_chart(fig_spend_map, use_container_width=True, key="intro_spending_map")

    st.info("""
    Metropolitan areas such as Île-de-France show higher average cultural spending, while rural or less connected regions spend less on average.  
                Spending patterns vary significantly across regions.  
    """)

    st.markdown("---")

    st.subheader("Project Information")
    st.info("""
    
    **Dataset:** Based on a national survey of cultural and digital consumption in France.  
    **Source:** [data.gouv.fr](https://www.data.gouv.fr/datasets/consommation-des-contenus-culturels-et-sportifs-numeriques-barometre/).  
    **License:** Open Data France.  
    **Productor:** Arcom - Autorité de Régulation de la Communication Audiovisuelle et Numérique      
    **Rows:** {}  
    **Columns:** {}  
    Missing values handled by imputation or category grouping.  
    """.format(df.shape[0], df.shape[1]))    
