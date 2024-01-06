import pandas as pd
import streamlit as st
from io import StringIO

def read_csv_sections(csv_content):
    sections = []
    lines = csv_content.strip().split('\n')
    
    # Split the lines into sections based on the start and end markers
    start_indices = [i for i, line in enumerate(lines) if line.startswith('# Start date:')]
    end_indices = [i for i, line in enumerate(lines) if line.startswith('# End date:')]
    
    # Iterate over each section and extract the data
    for start_index, end_index in zip(start_indices, end_indices):
        section_lines = lines[start_index:end_index]
        section_name = section_lines[2].split(':')[1].strip()  # Extract the section name from the third line
        
        # Remove leading and trailing whitespaces from each line
        section_lines = [line.strip() for line in section_lines]
        
        # Remove empty lines and extra header lines
        section_lines = [line for line in section_lines if line and not line.startswith('#')]
        
        # Create a DataFrame for the section
        section_df = pd.read_csv(StringIO('\n'.join(section_lines)), skipinitialspace=True)
        
        # Add the section name and DataFrame to the list of sections
        sections.append((section_name, section_df))
    
    return sections

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    csv_content = uploaded_file.read().decode('utf-8')
    sections = read_csv_sections(csv_content)
    
    # Render each section's DataFrame using Streamlit
    for section_name, section_df in sections:
        st.subheader(section_name)
        st.write(section_df)
