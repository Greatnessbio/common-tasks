import streamlit as st
import pandas as pd
from io import StringIO

# Function to split the CSV into sections and return a list of DataFrames
def split_csv_sections(uploaded_file):
    content = uploaded_file.getvalue().decode("utf-8")
    sections = content.split('\n#\n')

    data_sections = []

    for section in sections:
        if section.strip():
            section_io = StringIO(section)
            section_lines = section_io.readlines()
            section_name = section_lines[0].strip()  # Extract section name
            section_data = section_io.read()  # Read section data
            data_sections.append((section_name, section_data))
            
    return data_sections

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Sections")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    data_sections = split_csv_sections(uploaded_file)

    # Display individual DataFrames for each section with headers
    st.write("Individual DataFrames:")
    for section_name, section_data in data_sections:
        st.subheader(section_name)
        df = pd.read_csv(StringIO(section_data), sep='\t', skiprows=2)
        st.write(df)