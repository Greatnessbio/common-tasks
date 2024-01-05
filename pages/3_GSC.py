import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import StringIO

# Function to load the uploaded file into a DataFrame
def load_csv(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        return pd.read_csv(StringIO(bytes_data.decode('utf-8')))
    return None

# Function to generate summary visuals for a DataFrame
def generate_summary_visuals(df, df_name):
    st.subheader(f"Summary for {df_name}")
    st.dataframe(df)

    # Generate summary statistics for numerical columns
    st.subheader(f"Statistics for {df_name}")
    st.write(df.describe())

    # Visuals: pairplot for all numerical data
    try:
        numerical_df = df.select_dtypes(include=['float64', 'int64'])
        st.subheader(f"Pairplot for {df_name}")
        fig = sns.pairplot(numerical_df)
        st.pyplot(fig)
    except TypeError:
        st.write("No numerical data to display pairplot.")

    # Visuals: Bar plot for top 5 items based on a key metric
    key_metrics = ['Clicks', 'Impressions', 'CTR', 'Position']
    for metric in key_metrics:
        if metric in df.columns:
            st.subheader(f"Top 5 {metric} for {df_name}")
            fig, ax = plt.subplots()
            top_items = df.nlargest(5, metric)
            sns.barplot(x=metric, y=df.columns[0], data=top_items, ax=ax)
            st.pyplot(fig)

# Main app
def main():
    st.title("GSC Data Visualization App")

    # File Upload Interface
    uploaded_files = st.file_uploader("Upload CSV Files", type=['csv'], accept_multiple_files=True)

    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = load_csv(uploaded_file)
            if df is not None:
                generate_summary_visuals(df, uploaded_file.name)

if __name__ == "__main__":
    main()
