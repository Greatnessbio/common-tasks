import streamlit as st
import pandas as pd
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

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Sections")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    data_sections = split_csv_sections(uploaded_file)

    # Display individual DataFrames for each section with headers
    st.write("Individual DataFrames:")
    for idx, section_df in enumerate(data_sections, start=1):
        st.subheader(f"Section {idx}")
        st.write(section_df)
