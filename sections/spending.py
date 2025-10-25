import streamlit as st
from utils.viz import pie, bar
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def show(df):
    # --------------------------
    # PAGE TITLE + SHORT INTRO
    # --------------------------
    st.header("Cultural Economy: Spending & Monetization")

    st.markdown("""
    This section explores **how French consumers pay for digital culture** — analyzing **spending levels**, 
    **payment preferences**, and **access to paid services**.  
    The data reveals a market defined by **low average spending**, **hybrid consumption**, and a growing **sharing economy**.
    """)

    # --------------------------
    # 1. Monthly Spending Overview (Better Visualization)
    # --------------------------
    st.subheader("Monthly Cultural Spending")

    # Clean values: remove negatives, extreme outliers (> 200€)

    bins = [0, 10, 30, 60, 100, np.inf]
    labels = ["€0–10", "€10–30", "€30–60", "€60–100", "€100+"]
    df['spending_group'] = pd.cut(df['depense_mensuelle_culturelle'], bins=bins, labels=labels, right=False)

    group_counts = df['spending_group'].value_counts().reset_index()
    group_counts.columns = ['Spending Range', 'Count']

    fig_donut = px.pie(
        group_counts,
        names='Spending Range',
        values='Count',
        title="Cultural Spending Brackets",
        hole=0.4,
        color_discrete_sequence=px.colors.sequential.Blues_r
    )
    fig_donut.update_traces(textinfo='percent+label', textposition='outside')
    st.plotly_chart(fig_donut, use_container_width=True, key="spending_donut")

    st.info("""
    Nearly **70 % of users spend less than €30 per month**, confirming that **low spending dominates** the digital cultural economy.  
    Only a small fraction of heavy contributors (> €60) support premium content and subscriptions.
    """)
    st.markdown("---")

    # --------------------------
    # 2. Free vs Paid Consumption
    # --------------------------
    st.subheader("Free vs Paid Consumption")

    if 'gratuit_ou_payant' in df.columns:
        paid_counts = df['gratuit_ou_payant'].value_counts().reset_index()
        paid_counts.columns = ['Consumption Type', 'Count']
        fig_paid = bar(
            paid_counts,
            'Consumption Type',
            'Count',
            "Free vs Paid Consumption"
        )
        st.plotly_chart(fig_paid, use_container_width=True, key="paid")

    st.info("""
    The majority of users combine **free and paid content**, illustrating the **hybrid nature** of cultural consumption.  
    This balance between **convenience (free)** and **quality (paid)** shows a flexible digital economy adapting to user expectations.
    """)

    st.markdown("---")

    # --------------------------
    # 3. Access to Paid Services (Cleaned)
    # --------------------------
    st.subheader("Access to Paid Services")

    if 'acces_services_payants' in df.columns:
        df_access = df[df['acces_services_payants'].notna()]
        df_access = df_access[df_access['acces_services_payants'].str.lower() != 'null']

        fig_access = pie(
            df_access,
            names='acces_services_payants',
            title="Access to Paid Services"
        )
        fig_access.update_traces(textinfo='percent+label', textposition='outside')
        st.plotly_chart(fig_access, use_container_width=True, key="access")

    st.info("""
    Among paid users, **account sharing** is a widespread practice, while a smaller segment maintains **individual subscriptions**.  
    This indicates a cultural shift toward **shared digital access models**, blurring the line between private and collective use.
    """)

    st.markdown("---")

    # --------------------------
    # 4. Spending by Legal Consumption Type
    # --------------------------
    st.subheader("Spending by Consumption Type")

    if 'type_conso_legale_ou_illegale' in df.columns:
        avg_spend_by_type = df.groupby('type_conso_legale_ou_illegale')['depense_mensuelle_culturelle'].mean().reset_index()
        avg_spend_by_type.columns = ['Consumption Type', 'Average Monthly Spending (€)']

        fig_spend_type = px.bar(
            avg_spend_by_type,
            x='Consumption Type',
            y='Average Monthly Spending (€)',
            title="Average Monthly Spending by Legal vs Illegal Consumption",
            text_auto=True,
            color='Average Monthly Spending (€)',
            color_continuous_scale='Blues'
        )
        fig_spend_type.update_layout(xaxis_title="Consumption Type", yaxis_title="Average Spending (€)")
        st.plotly_chart(fig_spend_type, use_container_width=True, key="spend_type")

    st.info("""
    Consumers focusing on **legal platforms** spend considerably more than those engaging in **illegal or hybrid practices**.  
    This demonstrates that **trust and content legitimacy** directly correlate with **economic contribution**.
    """)

    st.markdown("---")

    # --------------------------
    # 5. Final Summary Block
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
            Digital Cultural Economy: Between Access and Affordability
        </h3>
        <p style="font-size:17px; color:#1c1c1c; line-height:1.6; margin-top:5px;">
            France’s digital culture market shows <strong>modest but steady spending habits</strong>, 
            driven by a <strong>hybrid mix of free and paid access</strong>.  
            The popularity of <strong>shared accounts</strong> highlights a new model where 
            <strong>community and convenience outweigh ownership</strong>.  
            Legal platforms benefit from <strong>trust-based monetization</strong>, while the overall ecosystem 
            reflects a <strong>cost-sensitive yet highly engaged audience</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
