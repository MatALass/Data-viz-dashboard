import streamlit as st
from utils.viz import pie, hist, bar, count_df
import plotly.express as px

def show(df):
    st.header("Who Are France’s Digital Culture Consumers?")

    st.markdown("""
    This section explores the demographic profile of French digital culture consumers,
    focusing on **gender, age, region, employment**, and **household structure**.
    """)

    # --------------------------
    # Demographic Breakdown
    # --------------------------
    st.subheader("Demographic Breakdown")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            pie(df, names='sexe', title="Gender Distribution"),
            use_container_width=True, key="gender"
        )
    with col2:
        st.plotly_chart(
            hist(df, x='age', title="Age Distribution (Respondents)"),
            use_container_width=True, key="age"
        )

    st.info("""
    The audience is almost evenly split between **men (48%) and women (52%)**, indicating that **digital cultural consumption in France is not gender-skewed**.  
    The **core age group (30–55 years)** dominates cultural consumption, showing that **digital habits are strongest among working-age adults** who combine **purchasing power** and **digital familiarity**.
    """)

    st.markdown("---")

    # --------------------------
    # Geographic Context
    # --------------------------
    st.subheader("Geographic and Urban Context")

    region_counts = count_df(df, 'region', 'Region')
    st.plotly_chart(
        bar(region_counts, 'Region', 'Count', "Respondents by Region"),
        use_container_width=True, key="region"
    )

    if 'type_agglomeration' in df.columns:
        agglo_counts = count_df(df, 'type_agglomeration', 'Agglomeration Type')
        st.plotly_chart(
            bar(agglo_counts, 'Agglomeration Type', 'Count', "Type of Urban Area"),
            use_container_width=True, key="agglo"
        )

    st.info("""
    Respondents are concentrated in **major urban and peri-urban areas**, with strong representation in **Île-de-France**, **Provence-Alpes-Côte d’Azur**, and **Pays de la Loire**.  
    Interestingly, a growing share comes from **rural zones**, suggesting that **digital access and cultural platforms now extend beyond metropolitan centers**.
    """)

    st.markdown("---")

    # --------------------------
    # Employment & Professional Status
    # --------------------------
    st.subheader("Employment and Professional Status")

    if 'statut_emploi' in df.columns:
        emploi_counts = count_df(df, 'statut_emploi', 'Employment Status')
        st.plotly_chart(
            bar(emploi_counts, 'Employment Status', 'Count', "Employment Status of Respondents"),
            use_container_width=True, key="employment"
        )

    if 'profession_principale' in df.columns and 'statut_emploi' in df.columns:
        fig_box = px.box(
            df,
            x='statut_emploi',
            y='age',
            title="Age Distribution by Employment Status",
            color='statut_emploi'
        )
        fig_box.update_layout(
            xaxis_title="Employment Status",
            yaxis_title="Age"
        )
        st.plotly_chart(fig_box, use_container_width=True, key="employment_age")

    st.info("""
    - Most participants are **private-sector employees** (“Salarié du privé ou association”), followed by **public-sector workers** and **self-employed individuals**.  
    - Younger respondents (**25–40 years old**) are concentrated in private employment, while **older groups** dominate public service and managerial roles.  
    - This indicates that **professional stability and digital adoption evolve with career stage**: mid-career workers remain the **most active online cultural consumers**.
    """)

    st.markdown("---")

    # --------------------------
    # Household Structure
    # --------------------------
    st.subheader("Household Structure")

    if 'taille_foyer' in df.columns:
        foyer_counts = count_df(df, 'taille_foyer', 'Household Size')
        st.plotly_chart(
            bar(foyer_counts, 'Household Size', 'Count', "Household Size Distribution"),
            use_container_width=True, key="household"
        )

    if 'statut_foyer' in df.columns:
        st.plotly_chart(
            pie(df, names='statut_foyer', title="Household Status (Single, Couple, etc.)"),
            use_container_width=True, key="household_status"
        )

    st.info("""
    - The majority live in **two-person households**, followed by **single** and **three-person households**, suggesting many **young couples or small families**.  
    - Over **60% identify as couples**, while **30% are single** and a small share are **children living with parents**.  
    - This composition supports the idea that **digital cultural spending is driven by adults with moderate family obligations and stable incomes**.
    """)

    st.markdown("---")

    # --------------------------
    # Insights — Styled Block
    # --------------------------
    st.markdown("""
    <div style="
        background-color:#E8F1FB;
        border-left: 6px solid #1E90FF;
        padding: 20px 25px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-top: 25px;
    ">
        <h3 style="color:#0E1117; font-weight:700; margin-bottom:8px;">
            The Typical Digital Culture Consumer
        </h3>
        <p style="font-size:17px; color:#1c1c1c; line-height:1.6; margin-top:5px;">
            In France, the <strong>typical digital culture consumer</strong> is a 
            <strong>30–50-year-old working adult</strong>, living in an 
            <strong>urban or semi-rural area</strong>, digitally connected, and financially active.  
            Their habits reflect both <strong>mainstream digital accessibility</strong> and 
            <strong>socio-economic stability</strong>, bridging <strong>rural and urban France</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
