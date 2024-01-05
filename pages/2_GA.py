import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Function to skip metadata and parse the actual data into a DataFrame
def parse_data_section(csv_content):
    # Skip metadata at the beginning of the CSV file
    header_row_index = None
    for i, row in enumerate(csv_content.split('\n')):
        if 'Nth day,Users' in row:  # This is our header row
            header_row_index = i
            break
            
    # If the header row is found, read the data into a DataFrame
    if header_row_index is not None:
        data = StringIO('\n'.join(csv_content.split('\n')[header_row_index:]))
        df = pd.read_csv(data, sep=',')
        return df
    else:
        return None

# Function to plot the data
def plot_data(df):
    if df is not None and not df.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df.iloc[:,0], df.iloc[:,1], marker='o')
        plt.title('User Acquisition Over Time')
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.grid(True)
        st.pyplot(plt)
    else:
        st.write("No data to plot.")

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Visualization")

# File uploader widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the content of the file
    content = uploaded_file.getvalue().decode("utf-8")
    
    # Parse the CSV content into a DataFrame
    data_df = parse_data_section(content)
    
    # Display the DataFrame
    if data_df is not None:
        st.write(data_df)
        
        # Plot the data
        plot_data(data_df)
    else:
        st.error("The data could not be parsed. Please check the CSV file format.")
