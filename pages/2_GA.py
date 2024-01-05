import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Function to split the CSV into sections and return a dictionary of DataFrames
def split_csv_sections(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    sections = content.split('#\n\n')
    data_sections = {}
    
    for section in sections:
        if section.strip():
            section_io = StringIO(section)
            section_df = pd.read_csv(section_io, sep='\t', skiprows=2)
            section_name = section_df.columns[0]
            data_sections[section_name] = section_df
            
    return data_sections

# Function to create a simple plot from a DataFrame
def create_plot(data_frame, title):
    plt.figure(figsize=(10, 4))
    for column in data_frame.columns[1:]:
        plt.plot(data_frame[data_frame.columns[0]], data_frame[column], label=column)
    plt.title(title)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Visualization")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    data_sections = split_csv_sections(uploaded_file)

    # Display individual DataFrames and Plots for each section
    for section_name, section_df in data_sections.items():
        st.subheader(section_name)
        st.write(section_df)

        # Plotting the data
        st.pyplot(create_plot(section_df, section_name))
