import pandas as pd
import streamlit as st

@st.cache_data(show_spinner="Loading dataset...", ttl=3600)
def load_data():
    """
    Loads and preprocesses the dataset.
    Cached for fast reloading when filters are changed.
    """
    df = pd.read_excel("data/data.xlsx")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Drop technical index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Clean categorical columns
    for col in ["region", "sexe"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 🧹 Fix 'age' properly
    if "age" in df.columns:
        # Remove all non-numeric characters (like "ans")
        df["age"] = df["age"].astype(str).str.extract(r"(\d+)")[0]
        # Convert to numeric (coerce invalid)
        df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Convert numeric columns to float32
    num_cols = df.select_dtypes(include="number").columns
    df[num_cols] = df[num_cols].astype("float32")

    return df
