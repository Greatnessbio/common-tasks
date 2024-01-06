import streamlit as st
import pandas as pd
from datetime import datetime

def parse_metadata(lines):
    metadata = {}
    for line in lines:
        if line.startswith('#'):
            parts = line.strip('# ').split(': ')
            if len(parts) == 2:
                key, value = parts
                metadata[key.replace(' ', '_').lower()] = value
    return metadata

def parse_date(date_str):
    return datetime.strptime(date_str, '%Y%m%d').date()

def parse_sections(lines, metadata):
    sections = {}
    current_section = None
    section_data = []
    headers = []

    for line in lines:
        if not line.strip() or line.startswith('#'):
            continue  # Skip metadata or empty lines
        if ',' in line and not any(char.isdigit() for char in line):
            # This is a header line
            if current_section and section_data:
                sections[current_section] = pd.DataFrame(section_data, columns=headers)
            current_section = line.strip()
            section_data = []
            headers = line.split(',')
        elif ',' in line:
            # This is a data line
            section_data.append(line.split(','))

    # Add the last section
    if current_section and section_data:
        sections[current_section] = pd.DataFrame(section_data, columns=headers)

    return sections

def process_csv(content):
    lines = content.split('\n')
    metadata = parse_metadata(lines[:10])  # adjust based on actual metadata lines in file
    sections = parse_sections(lines[10:], metadata)  # adjust based on actual data start in file
    
    # Convert 'Nth day' to dates
    for section_name, df in sections.items():
        if 'Nth day' in df.columns:
            start_date = parse_date(metadata['start_date'])
            df['Nth day'] = pd.to_numeric(df['Nth day']).apply(lambda x: start_date + pd.Timedelta(days=x))
            df.rename(columns={'Nth day': 'Date'}, inplace=True)
    
    return sections

# Streamlit UI
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        content = uploaded_file.getvalue().decode('utf-8')
        sections = process_csv(content)

        for section_name, df in sections.items():
            st.subheader(section_name)
            st.dataframe(df)

    except Exception as e:
        st.error(f"An error occurred: {e}")
else:
    st.info("Please upload a CSV file.")
