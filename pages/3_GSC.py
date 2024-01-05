import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

# Function to load the uploaded file into a DataFrame
def load_csv(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        df = pd.read_csv(StringIO(bytes_data.decode('utf-8')))
        # Clean CTR column if it exists and contains percentages
        if 'CTR' in df.columns:
            df['CTR'] = df['CTR'].str.rstrip('%').astype('float') / 100.0
        # Clean Position column to be numeric
        if 'Position' in df.columns:
            df['Position'] = pd.to_numeric(df['Position'], errors='coerce')
        return df
    return None

# Function to generate summary visuals for a DataFrame
def generate_summary_visuals(df, df_name):
    st.subheader(f"Data Summary for {df_name}")
    st.dataframe(df)
    st.write(df.describe())

    # Visualizations
    if 'Clicks' in df.columns:
        st.subheader(f"Clicks Distribution for {df_name}")
        fig, ax = plt.subplots()
        sns.histplot(df['Clicks'], kde=False, ax=ax)
        st.pyplot(fig)

    if 'Impressions' in df.columns:
        st.subheader(f"Impressions Distribution for {df_name}")
        fig, ax = plt.subplots()
        sns.histplot(df['Impressions'], kde=False, ax=ax)
        st.pyplot(fig)

    if 'CTR' in df.columns:
        st.subheader(f"CTR Distribution for {df_name}")
        fig, ax = plt.subplots()
        sns.histplot(df['CTR'], kde=True, ax=ax)
        st.pyplot(fig)

    if 'Position' in df.columns:
        st.subheader(f"Position Distribution for {df_name}")
        fig, ax = plt.subplots()
        sns.histplot(df['Position'], kde=True, ax=ax)
        st.pyplot(fig)

# Streamlit application layout
def main():
    st.title("GSC Data Visualization App")

    # File Upload Interface
    uploaded_files = st.file_uploader("Upload CSV Files", type=['csv'], accept_multiple_files=True)

    if uploaded_files:
        # Process each file
        for uploaded_file in uploaded_files:
            df = load_csv(uploaded_file)
            if df is not None:
                generate_summary_visuals(df, uploaded_file.name)

if __name__ == "__main__":
    main()
