import streamlit as st
import pandas as pd
import os

def process_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1]

    if file_extension.lower() == '.xlsx':
        df = pd.read_excel(uploaded_file, engine='openpyxl')
    elif file_extension.lower() == '.xls':
        # For '.xls' files, use an appropriate engine like 'xlrd' (version 1.2.0 or earlier)
        df = pd.read_excel(uploaded_file, engine='xlrd')  # Ensure you have the compatible version of xlrd

    # Process and split the DataFrame
    for name, group in df.groupby('ColumnName'):
        # Save each group to a CSV file
        group.to_csv(f'{name}.csv', index=False)
        st.success(f'File saved: {name}.csv')

def main():
    st.title("LinkedIn Excel to CSV Processor")

    # File uploader that accepts both .xlsx and .xls files
    uploaded_file = st.file_uploader("Upload your LinkedIn Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        process_file(uploaded_file)

if __name__ == "__main__":
    main()
