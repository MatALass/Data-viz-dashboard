import streamlit as st
from sections import intro, profile, behavior, spending, insights
from utils.io import load_data

# --------------------------
# Page config
# --------------------------
st.set_page_config(
    page_title="Digital Culture in France",
    layout="wide",
    page_icon="📊"
)

# --------------------------
# Load Data (with caching)
# --------------------------
@st.cache_data
def get_data():
    return load_data()

df = get_data()
# --------------------------
# Custom CSS (modern sidebar + styled filters)
# --------------------------
st.markdown("""
<style>
/* === SIDEBAR BACKGROUND === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2540 0%, #133b66 100%) !important;
    padding-top: 2rem;
}
[data-testid="stSidebar"] * {color: white !important;}
[data-testid="stSidebar"] h3 {
    text-align: center;
    font-weight: 700;
    font-size: 18px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 1rem;
}

/* === RADIO BUTTONS === */
[data-testid="stSidebar"] .stRadio label {
    color: white !important;
    font-weight: 500;
    font-size: 15px !important;
    border-radius: 8px;
    padding: 6px 10px;
    transition: all 0.2s ease;
}
[data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background-color: #ffffff !important;
    color: #0A2540 !important;
    font-weight: 700 !important;
}

/* === SELECTBOX BEAUTIFIED === */
div[data-baseweb="select"] {
    background: rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    transition: all 0.3s ease;
}
div[data-baseweb="select"]:hover {
    background: rgba(255,255,255,0.25) !important;
}
div[data-baseweb="select"] > div {
    color: #FFFFFF !important; /* texte dans la zone */
    font-weight: 600 !important;
    font-size: 14px !important;
}
div[role="listbox"] div[role="option"] {
    color: #0A2540 !important;
    background-color: #ffffff !important;
    font-size: 14px !important;
}
div[role="listbox"] div[role="option"]:hover {
    background-color: rgba(10,37,64,0.08) !important;
}
svg[data-testid="stSelectboxCaret"] path {
    fill: #FFFFFF !important;
}

/* === FILTER TAGS DISPLAY === */
.filter-tag {
    background-color: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.3);
    border-radius: 8px;
    padding: 8px 10px;
    margin-top: 10px;
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 500;
    line-height: 1.4;
}
.filter-tag span {
    color: #7FDBFF;
    font-weight: 600;
}
footer, header, #MainMenu {visibility: hidden !important;}
</style>
""", unsafe_allow_html=True)

# --------------------------
# Sidebar Navigation + Filters
# --------------------------
st.sidebar.image("assets/logo.png", use_container_width=True)
st.sidebar.markdown("<h3>Digital Culture Dashboard</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='border:1px solid rgba(255,255,255,0.25);'>", unsafe_allow_html=True)

# --- Filters ---
st.sidebar.markdown("### Filters")

regions = ["All"] + sorted(df["region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions, key="filter_region")

sexes = ["All"] + sorted(df["sexe"].dropna().unique().tolist())
selected_sex = st.sidebar.selectbox("Gender", sexes, key="filter_gender")

# Apply filters globally
filtered_df = df.copy()
if selected_region != "All":
    filtered_df = filtered_df[filtered_df["region"] == selected_region]
if selected_sex != "All":
    filtered_df = filtered_df[filtered_df["sexe"] == selected_sex]

# Display current selections beautifully
st.sidebar.markdown(
    f"""
    <div class="filter-tag">
        <strong>Current Selection</strong><br>
        Region: <span>{selected_region}</span><br>
        Gender: <span>{selected_sex}</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("<hr style='border:1px solid rgba(255,255,255,0.25); margin-top:1rem;'>", unsafe_allow_html=True)


# --- Page Navigation ---
page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Audience Profile",
        "Online Habits",
        "Cultural Economy",
        "Key Findings"
    ],
    label_visibility="collapsed",
    key="main_navigation"
)

st.sidebar.markdown(
    "<p style='text-align:center; font-size:13px; color:rgba(255,255,255,0.7); margin-top:10px;'>© 2025 EFREI Mathieu ALASSOEUR</p>",
    unsafe_allow_html=True
)

# --------------------------
# Routing (pass filtered_df)
# --------------------------
with st.spinner("Updating dashboard..."):
    if page == "Overview":
        intro.show(filtered_df)
    elif page == "Audience Profile":
        profile.show(filtered_df)
    elif page == "Online Habits":
        behavior.show(filtered_df)
    elif page == "Cultural Economy":
        spending.show(filtered_df)
    elif page == "Key Findings":
        insights.show(filtered_df)
