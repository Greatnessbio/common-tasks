import streamlit as st
import pandas as pd
import os

def process_file(uploaded_file):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)

    # Process and split the DataFrame (this is just a placeholder, adjust as needed)
    # Example: Splitting based on a column
    for name, group in df.groupby('ColumnName'):
        # Save each group to a CSV file
        group.to_csv(f'{name}.csv', index=False)
        st.success(f'File saved: {name}.csv')

def main():
    st.title("LinkedIn Excel to CSV Processor")

    # File uploader
    uploaded_file = st.file_uploader("Upload your LinkedIn Excel file", type=["xlsx"])

    if uploaded_file is not None:
        process_file(uploaded_file)

if __name__ == "__main__":
    main()
