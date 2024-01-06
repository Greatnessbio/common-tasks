import streamlit as st
import pandas as pd
from datetime import datetime

def parse_metadata(lines):
    metadata = {}
    for line in lines:
        if line.startswith('#'):
            key, value = line.strip('# ').split(': ')
            metadata[key.replace(' ', '_').lower()] = value
    return metadata

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d').date()

def parse_sections(lines, metadata):
    sections = {}
    current_section = None
    section_data = []

    for line in lines:
        if not line.strip() or line.startswith('#'):
            # This is a blank line or a metadata line, skip it
            continue
        if ',' not in line:
            # This looks like a section header
            if current_section and section_data:
                # Save the previous section
                sections[current_section] = pd.DataFrame(section_data[1:], columns=section_data[0])
                section_data = []
            current_section = line.strip()
        else:
            # This is a data line
            section_data.append(line.split(','))

    # Don't forget to add the last section
    if current_section and section_data:
        sections[current_section] = pd.DataFrame(section_data[1:], columns=section_data[0])

    return sections

def process_csv(content):
    lines = content.split('\n')
    metadata = parse_metadata(lines[:5])  # assuming the first 5 lines are metadata
    start_date = parse_date(metadata['start_date'])
    sections = parse_sections(lines[5:], metadata)
    
    # Convert 'Nth day' to dates
    for section_name, df in sections.items():
        if 'Nth day' in df.columns:
            df['Nth day'] = df['Nth day'].astype(int).apply(lambda x: start_date + pd.Timedelta(days=x))
            df.rename(columns={'Nth day': 'Date'}, inplace=True)
            
    return sections

# Streamlit UI
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        # Read the content of the file
        content = uploaded_file.getvalue().decode('utf-8')
        sections = process_csv(content)

        for section_name, df in sections.items():
            st.subheader(section_name)
            st.dataframe(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV file.")
