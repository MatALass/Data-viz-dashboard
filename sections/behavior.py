import streamlit as st
from utils.viz import hist, bar
import plotly.express as px
import pandas as pd

def show(df):
    # --------------------------
    # PAGE TITLE + SHORT INTRO
    # --------------------------
    st.header("Digital Behaviors and Cultural Practices")

    st.markdown("""
    Beyond demographics, digital habits reveal how French consumers **access, protect, and engage with online culture**.  
    This section examines **connectivity levels, security practices, and consumption behaviors** from VPN usage to content legality.
    """)

    # --------------------------
    # 1. Internet Usage Frequency
    # --------------------------
    st.subheader("Internet Usage Frequency")

    if 'frequence_internet' in df.columns:
    # Compte + pourcentage
        freq_counts = (
            df['frequence_internet']
            .value_counts(normalize=True)
            .mul(100)
            .reset_index()
        )
        freq_counts.columns = ['Internet Usage Frequency', 'Percentage']

        # Conversion propre en numérique
        freq_counts['Percentage'] = pd.to_numeric(freq_counts['Percentage'], errors='coerce')

        # Tri logique du plus fréquent au moins fréquent
        freq_counts = freq_counts.sort_values('Percentage', ascending=False)

        # Création du graphe horizontal
        fig_freq = px.bar(
            freq_counts,
            x='Percentage',
            y='Internet Usage Frequency',
            orientation='h',
            text=freq_counts['Percentage'].map(lambda x: f"{x:.1f}%" if pd.notna(x) else ""),
            title="How Often Respondents Use the Internet",
            color='Percentage',
            color_continuous_scale='Blues'
        )

        fig_freq.update_layout(
            xaxis_title="Percentage of Respondents",
            yaxis_title="",
            xaxis=dict(showgrid=True, ticksuffix="%"),
            yaxis=dict(autorange="reversed"),  # pour afficher le plus haut en haut
        )

        st.plotly_chart(fig_freq, use_container_width=True, key="internet_freq")

    # Nouveau texte d’analyse cohérent avec les données
    st.info("""
    Nearly **nine out of ten respondents** use the Internet **daily or several times a day**.  
    This confirms that **digital connectivity has become fully integrated** into everyday life in France where being online is now the default state rather than the exception.
    """)






    st.markdown("---")

    # --------------------------
    # 2. VPN Usage — Donut Chart (harmonized)
    # --------------------------
    st.subheader("VPN Usage")

    if 'utilisation_vpn' in df.columns:
        vpn_counts = df['utilisation_vpn'].value_counts().reset_index()
        vpn_counts.columns = ['VPN Usage', 'Count']
        fig_vpn = px.pie(
            vpn_counts,
            names='VPN Usage',
            values='Count',
            title="VPN Usage Among Respondents",
            hole=0.5,
            color_discrete_sequence=px.colors.sequential.Blues_r
        )
        fig_vpn.update_traces(
            textinfo='percent+label',
            textposition='outside',
            textfont_size=14,
            pull=[0.05] * len(vpn_counts)
        )
        fig_vpn.update_layout(showlegend=True)
        st.plotly_chart(fig_vpn, use_container_width=True, key="vpn")

    st.info("""  
    VPN usage remains **limited**, with the majority never using one.  
    However, a small segment of **digitally-aware users** adopts VPNs to enhance privacy or bypass regional restrictions.
    """)

    st.markdown("---")

    # --------------------------
    # 3. Cracked Apps Usage — Grouped Bar Chart
    # --------------------------
    st.subheader("Cracked Apps Usage vs Gender")

    if 'utilisation_applis_crackees' in df.columns and 'sexe' in df.columns:
        cracked_counts = df.groupby(['utilisation_applis_crackees', 'sexe']).size().reset_index(name='Count')
        fig_crack = px.bar(
            cracked_counts,
            x='utilisation_applis_crackees',
            y='Count',
            color='sexe',
            barmode='group',
            title="Cracked Apps Usage by Gender",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_crack.update_layout(
            xaxis_title="Cracked Apps Usage Frequency",
            yaxis_title="Number of Respondents"
        )
        st.plotly_chart(fig_crack, use_container_width=True, key="cracked_apps")

    st.info("""  
    Using cracked apps remains **marginal overall**, with slightly higher rates among men.  
    This behavior is typically linked to **younger, more tech-savvy users** who explore free access alternatives.
    """)

    st.markdown("---")

    # --------------------------
    # 4. Legal vs Illegal Consumption — Stacked Bar
    # --------------------------
    st.subheader("Legal vs. Illegal Consumption by Frequency")

    if 'type_conso_legale_ou_illegale' in df.columns and 'frequence_conso_culturelle' in df.columns:
        cross = pd.crosstab(df['frequence_conso_culturelle'], df['type_conso_legale_ou_illegale'])
        cross = cross.reset_index().melt(id_vars='frequence_conso_culturelle', var_name='Type', value_name='Count')

        fig_stack = px.bar(
            cross,
            x='frequence_conso_culturelle',
            y='Count',
            color='Type',
            title="Frequency of Cultural Consumption by Legal/Illegal Access",
            text_auto=True,
            barmode='stack',
            color_discrete_sequence=px.colors.sequential.Blues
        )
        fig_stack.update_layout(
            xaxis_title="Frequency of Cultural Consumption",
            yaxis_title="Number of Respondents"
        )
        st.plotly_chart(fig_stack, use_container_width=True, key="stacked_legal")

    st.info("""  
    Most respondents primarily rely on **legal or mixed (hybrid)** platforms for cultural consumption.  
    Fully illegal practices are **rare and declining**, indicating growing preference for accessible, legitimate content.
    """)

    st.markdown("---")

    # --------------------------
    # 5. Streaming/Downloading Behavior — Horizontal Bar
    # --------------------------
    st.subheader("Streaming or Downloading Habits")

    if 'utilisation_telechargement_streaming' in df.columns:
        stream_counts = df['utilisation_telechargement_streaming'].value_counts().reset_index()
        stream_counts.columns = ['Streaming/Downloading Behavior', 'Count']
        fig_stream = px.bar(
            stream_counts,
            x='Count',
            y='Streaming/Downloading Behavior',
            orientation='h',
            title="Streaming and Downloading Habits",
            text_auto=True,
            color='Count',
            color_continuous_scale='Blues'
        )
        fig_stream.update_layout(
            xaxis_title="Number of Respondents",
            yaxis_title="Streaming / Downloading Frequency"
        )
        st.plotly_chart(fig_stream, use_container_width=True, key="streaming_behavior")

    st.info("""  
    Streaming dominates over downloading, showing a **shift toward on-demand, always-connected access**.  
    Occasional downloads remain but are mostly performed by **older respondents** or those with limited connection stability.
    """)

    st.markdown("---")

    # --------------------------
    # FINAL INSIGHT BLOCK
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
            Digital Culture Consumption Patterns
        </h3>
        <p style="font-size:17px; color:#1c1c1c; line-height:1.6; margin-top:5px;">
            Digital cultural consumption in France is characterized by 
            <strong>constant Internet connectivity</strong>, 
            <strong>low but rising VPN awareness</strong>, and 
            <strong>predominantly legal streaming practices</strong>.  
            A minority of younger users explore cracked apps or hybrid content sources, 
            but the overall trend highlights a 
            <strong>mature, responsible, and convenience-driven audience</strong> 
            that embraces digital access while staying largely within legal frameworks.
        </p>
    </div>
    """, unsafe_allow_html=True)
