import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create a Streamlit app
st.title("CSV Data Explorer")

# Allow the user to upload multiple CSV files
uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

# Create a dictionary to store dataframes
dfs = {}

# Check if files have been uploaded
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read each uploaded CSV file into a separate dataframe
        df = pd.read_csv(uploaded_file)
        file_name = uploaded_file.name

        # Store the dataframe in the dictionary with the file name as the key
        dfs[file_name] = df

# Sidebar for data exploration
st.sidebar.title("Data Exploration")

# Display options for selecting a CSV file's dataframe
selected_file = st.sidebar.selectbox("Select a CSV file", list(dfs.keys()))

# Display options for filtering and sorting
st.sidebar.subheader("Filter and Sort Options")

# Filter by column values
for column in dfs[selected_file].columns:
    filter_value = st.sidebar.text_input(f"Filter {column}")
    if filter_value:
        dfs[selected_file] = dfs[selected_file][dfs[selected_file][column].astype(str).str.contains(filter_value, case=False, na=False)]

# Sort by column
sort_column = st.sidebar.selectbox("Sort by column", dfs[selected_file].columns)
dfs[selected_file] = dfs[selected_file].sort_values(sort_column, ascending=True)

# Display the selected dataframe
st.subheader(f"Data from {selected_file}")
st.write(dfs[selected_file])

# Chart area
st.subheader("Chart Area")

# Select columns for visualization
selected_columns = st.multiselect("Select columns for visualization", dfs[selected_file].columns)

# Choose chart type
chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart", "Scatter Plot"])

# Create charts based on user selections
if selected_columns and chart_type:
    chart_data = dfs[selected_file][selected_columns]
    st.write(f"### {chart_type} of Selected Columns")
    
    if chart_type == "Bar Chart":
        st.bar_chart(chart_data)
    elif chart_type == "Line Chart":
        st.line_chart(chart_data)
    elif chart_type == "Scatter Plot":
        st.scatter_chart(chart_data)
