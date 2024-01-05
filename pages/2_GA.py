import pandas as pd
import streamlit as st

# Upload the CSV file
uploaded_file = st.file_uploader("Upload your CSV file here...", type='csv')

if uploaded_file is not None:
    # Read the entire CSV file
    data = pd.read_csv(uploaded_file)

    # Find the indices of the headers
    headers = ["Nth day\tUsers", "Nth day\tNew users", "First user default channel group\tNew users", 
               "Session default channel group\tSessions", "Session Google Ads campaign\tSessions", "Cohort\tLTV"]
    indices = {header: data.index[data[0] == header][0] for header in headers}

    # Create a dictionary of DataFrames
    dfs = {}
    for i, header in enumerate(headers):
        start = indices[header] + 1
        end = indices[headers[i + 1]] if i + 1 < len(headers) else len(data)
        dfs[header] = pd.DataFrame(data[start:end][0].str.split('\t').tolist(), columns=data.iloc[start - 1][0].split('\t'))

    # Display the DataFrames
    for header, df in dfs.items():
        st.write(f"DataFrame for {header}:")
        st.dataframe(df)
