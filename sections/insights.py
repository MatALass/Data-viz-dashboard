import streamlit as st
import plotly.express as px
import pandas as pd

def show(df):
    # --------------------------
    # CLEAN & SAFEGUARD AGE COLUMN
    # --------------------------
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')  # force en numérique
        df = df[df['age'].notna()]  # supprime les NaN éventuels

    # --------------------------
    # PAGE HEADER
    # --------------------------
    st.header("Insights & Implications")

    st.markdown("""
    This final section connects **behavioral patterns**, **spending habits**, and **privacy awareness**  
    to draw a clear picture of how French audiences engage with digital culture today.
    """)

    # --------------------------
    # 1. Average Spending by Consumption Frequency
    # --------------------------
    st.subheader("Average Monthly Spending by Cultural Consumption Frequency")

    avg_by_freq = (
        df.groupby('frequence_conso_culturelle')['depense_mensuelle_culturelle']
        .mean().reset_index()
        .sort_values('depense_mensuelle_culturelle', ascending=False)
    )

    fig_bar = px.bar(
        avg_by_freq,
        x='frequence_conso_culturelle',
        y='depense_mensuelle_culturelle',
        title="Average Monthly Spending by Cultural Consumption Frequency",
        text_auto=True,
        color='depense_mensuelle_culturelle',
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(
        xaxis_title="Cultural Consumption Frequency",
        yaxis_title="Average Monthly Spending (€)"
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="spend_freq")

    st.info("""
    Frequent cultural consumers tend to spend more overall.  
    Regular engagement is closely tied to higher investment, 
    confirming that **habitual cultural activity directly drives economic value**.
    """)

    st.markdown("---")

    # --------------------------
    # 2. Spending by Age Group
    # --------------------------
    st.subheader("Average Cultural Spending by Age Group")

    if 'age' in df.columns:
        # 🧹 Clean and filter valid age range
        df_age = df[df['age'].between(15, 80, inclusive='both')]

        if not df_age.empty:
            df_age['age_group'] = pd.cut(
                df_age['age'],
                bins=[15, 25, 35, 45, 55, 65, 80],
                labels=["15–24", "25–34", "35–44", "45–54", "55–64", "65+"]
            )

            avg_spend_age = (
                df_age.groupby('age_group')['depense_mensuelle_culturelle']
                .mean()
                .reset_index()
            )

            fig_age = px.bar(
                avg_spend_age,
                x='age_group',
                y='depense_mensuelle_culturelle',
                title="Average Monthly Cultural Spending by Age Group",
                text_auto=True,
                color='depense_mensuelle_culturelle',
                color_continuous_scale='Blues'
            )
            fig_age.update_layout(
                xaxis_title="Age Group",
                yaxis_title="Average Spending (€)"
            )
            st.plotly_chart(fig_age, use_container_width=True, key="spending_age")

    st.info("""
    Adults aged **30 to 55** are the backbone of the digital cultural economy.  
    They combine **financial stability** and **digital fluency**, 
    while younger users show strong engagement but limited financial contribution.
    """)

    st.markdown("---")

    # --------------------------
    # 3. Key Takeaways (Compact layout)
    # --------------------------
    st.subheader("Key Insights")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **More activity → more spending**, regardless of VPN use.  
        - **Hybrid models** (free + paid) dominate digital culture.  
        - **Middle-aged audiences** drive the market’s revenue.  
        """)
    with col2:
        st.markdown("""
        - **Younger users** engage often but spend less.  
        - **Privacy awareness** doesn’t reduce payment behavior.  
        - **Account sharing** reshapes traditional monetization.  
        """)

    st.markdown("---")

    # --------------------------
    # 4. Implications
    # --------------------------
    st.subheader("What This Means")

    st.markdown("""
    **For Platforms:**  
    Strengthen **freemium and hybrid strategies** to capture both low and high spenders.  

    **For Cultural Policy:**  
    Encourage **equitable digital access** and support regional inclusion in legal streaming services.  

    **For Researchers:**  
    Study how **trust, privacy, and spending** interact to shape cultural engagement across age groups.
    """)

    st.markdown("---")

    # --------------------------
    # 5. Final Summary Block
    # --------------------------
    st.markdown("""
    <div style="
        background-color:#E8F1FB;
        border-left: 6px solid #1E90FF;
        padding: 25px 25px;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin-top: 25px;
    ">
        <h3 style="color:#0E1117; font-weight:700; margin-bottom:10px;">
            Looking Beyond the Data
        </h3>
        <p style="font-size:17px; color:#1c1c1c; line-height:1.6; margin-top:5px;">
            Behind every number lies a familiar story: people who stream, share, and pay for what moves them.  
            Digital culture in France is not defined by the platforms themselves, but by how audiences <strong>adapt, mix, and create their own balance</strong> 
            between access, ethics, and convenience.  
            This balance is where the future of cultural engagement and its value truly lives.
        </p>
    </div>
    """, unsafe_allow_html=True)
