import pandas as pd
import streamlit as st
from io import StringIO

def read_section(file, start_line):
    lines = []
    line = file.readline()
    while line.strip() != '':
        lines.append(line)
        line = file.readline()
    return pd.read_csv(StringIO(''.join(lines)), skipinitialspace=True)

# Upload the CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
    # Read the entire CSV file
    file_content = uploaded_file.readlines()

    # Create a dictionary of DataFrames
    dfs = {}
    i = 0
    while i < len(file_content):
        line = file_content[i].decode()
        if line.startswith('Nth day') or line.startswith('First user default channel group') or line.startswith('Session default channel group') or line.startswith('Session Google Ads campaign') or line.startswith('Cohort'):
            df = read_section(file_content[i:], i)
            dfs[line.strip()] = df
            i += len(df) + 2  # Skip the empty line after each section
        else:
            i += 1

    # Display the DataFrames
    for header, df in dfs.items():
        st.write(f"DataFrame for {header}:")
        st.dataframe(df)
