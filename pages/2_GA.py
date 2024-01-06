import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

def parse_date(date_str):
    # Trim the date string to remove any unexpected whitespace or newline characters
    return datetime.strptime(date_str.strip(), '%Y%m%d')

def read_csv_section(section_lines, start_date):
    # Assume the first line is the header
    header = section_lines[0]
    
    # Create DataFrame from section lines
    df = pd.read_csv(StringIO('\n'.join(section_lines[1:])), sep='\t', header=None)
    df.columns = header.split('\t')

    # Convert 'Nth day' to actual dates if it's in the DataFrame
    if 'Nth day' in df.columns:
        df['Date'] = df['Nth day'].apply(lambda x: start_date + timedelta(days=int(x)))

    return df

def process_csv_file(file_content):
    sections_data = {}
    lines = file_content.strip().split('\n')
    
    # Initialize variables to hold the start dates and section headers
    start_date = None
    section_header = None
    section_lines = []

    for line in lines:
        # Check for start date metadata
        if line.startswith('# Start date:'):
            # Parse the start date
            start_date_str = line.split(': ')[1]
            start_date = parse_date(start_date_str)
        elif line.startswith('# End date:'):
            # Skip end date line
            continue
        elif line.startswith('Nth day') or line.startswith('First user') or line.startswith('Session'):
            # If we encounter a new section header and there are existing section lines, process them
            if section_header and section_lines:
                df = read_csv_section(section_lines, start_date)
                sections_data[section_header] = df
                section_lines = []
            # Update the section header
            section_header = line
        elif line.strip() == '':
            # Skip empty lines
            continue
        else:
            # This must be a line of data; add it to the current section
            section_lines.append(line)

    # After the loop, process the last section if it exists
    if section_header and section_lines:
        df = read_csv_section(section_lines, start_date)
        sections_data[section_header] = df

    return sections_data

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        file_content = uploaded_file.getvalue().decode('utf-8')
        sections_data = process_csv_file(file_content)

        for section_name, df in sections_data.items():
            st.write(f"Section: {section_name}")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file.")
