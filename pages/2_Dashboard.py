import streamlit as st
import pandas as pd

# Create a Streamlit app
st.title("Google Search Console Data")

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

    # Display a dropdown to select the dataframe
    selected_df = st.selectbox("Select a DataFrame", list(dfs.keys()))

    # Display the selected dataframe
    st.subheader(f"Data from {selected_df}")
    st.write(dfs[selected_df])

    # Create charts or visualizations for the selected dataframe
    st.subheader(f"Chart for {selected_df}")
    # Add your charting code here using dfs[selected_df] as the dataframe
