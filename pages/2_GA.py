import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# Function to split the CSV into sections and return a list of DataFrames
def split_csv_sections(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    sections = content.split('#\n\n')

    data_sections = []

    for section in sections:
        if section.strip():
            section_io = StringIO(section)
            section_df = pd.read_csv(section_io, sep='\t', skiprows=2)
            data_sections.append(section_df)
            
    return data_sections

# Function to plot the data from a DataFrame
def plot_data(df):
    if df.shape[1] == 2:
        plt.figure(figsize=(8, 6))
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o')
        plt.xlabel(df.columns[0])
        plt.ylabel(df.columns[1])
        plt.title(f"Plot for {df.columns[0]} vs {df.columns[1]}")
        st.pyplot()

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Sections")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    data_sections = split_csv_sections(uploaded_file)

    # Display individual DataFrames for each section with headers
    st.write("Individual DataFrames:")
    for section_df in data_sections:
        st.subheader("Section")
        st.write(section_df)

    # Plot the data
    for section_df in data_sections:
        if section_df.shape[1] == 2:
            plot_data(section_df)
