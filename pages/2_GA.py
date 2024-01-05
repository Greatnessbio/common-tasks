import streamlit as st
import pandas as pd

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Identify unique sets of data based on combinations of values in multiple columns
    unique_sets = df.groupby(list(df.columns)).size().reset_index(name='count')
    unique_sets = unique_sets[unique_sets['count'] > 1].drop('count', axis=1)  # Keep only those with multiple occurrences

    # Create separate tables for each unique set
    for index, row in unique_sets.iterrows():
        filtered_df = df.loc[(df[row[0]] == row[1]) & (df[row[2]] == row[3])]  # Filter based on all column values
        st.subheader(f"Table for unique combination: {row.to_list()}")
        st.dataframe(filtered_df)
        st.markdown("---")  # Separator between tables

else:
    st.write("Please upload a CSV file to proceed.")
