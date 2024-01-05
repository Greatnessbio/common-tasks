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
        return df
    return None

# Function to generate appropriate visuals for a DataFrame
def generate_visuals(df, df_name):
    st.subheader(f"Data Summary for {df_name}")
    st.dataframe(df.head())

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        st.line_chart(df.set_index('Date')[['Clicks', 'Impressions', 'CTR', 'Position']])
    
    if 'Country' in df.columns or 'Device' in df.columns or 'Search Appearance' in df.columns:
        category = 'Country' if 'Country' in df.columns else ('Device' if 'Device' in df.columns else 'Search Appearance')
        clicks_by_category = df.groupby(category)['Clicks'].sum().sort_values(ascending=False)
        impressions_by_category = df.groupby(category)['Impressions'].sum().sort_values(ascending=False)
        st.bar_chart(clicks_by_category)
        st.bar_chart(impressions_by_category)
    
    if 'Queries' in df_name:
        st.bar_chart(df.set_index('Top queries')['Clicks'])
        st.bar_chart(df.set_index('Top queries')['Impressions'])

    if 'Pages' in df_name:
        st.bar_chart(df.set_index('Top pages')['Clicks'])
        st.bar_chart(df.set_index('Top pages')['Impressions'])

# Main Streamlit app
def main():
    st.title("GSC Data Visualization App")

    uploaded_files = st.file_uploader("Upload CSV Files", type=['csv'], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = load_csv(uploaded_file)
            if df is not None:
                generate_visuals(df, uploaded_file.name)

if __name__ == "__main__":
    main()
