import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Function to find the start of the actual data in the CSV file and parse it
def parse_csv(uploaded_file):
    # Decode the uploaded file
    file_content = uploaded_file.getvalue().decode("utf-8")
    # Split the content into lines
    lines = file_content.split('\n')
    # Find the start of the data section (after headers)
    for i, line in enumerate(lines):
        if 'Nth day,Users' in line:  # This identifies the header of the data section
            header_line = i
            break
    else:
        st.error("Data header not found.")
        return None

    # Extract the data section
    data_lines = lines[header_line:]
    data_str = '\n'.join(data_lines)
    data_io = StringIO(data_str)

    # Use the first line as header and read the rest of the lines as data
    df = pd.read_csv(data_io, header=0)
    return df

# Function to create a plot from the DataFrame
def create_plot(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df['Nth day'], df['Users'], marker='o')
    plt.title('User Acquisition Over Time')
    plt.xlabel('Nth Day')
    plt.ylabel('Users')
    plt.tight_layout()
    return plt

# Streamlit app layout
st.title("Google Analytics Data Visualization")

# File uploader widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    # Parse the uploaded CSV file
    df = parse_csv(uploaded_file)
    
    if df is not None:
        # Display the DataFrame
        st.write(df)

        # Create and display the plot
        st.pyplot(create_plot(df))
