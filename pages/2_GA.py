import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

# Helper function to parse dates.
def parse_date(date_str):
    return datetime.strptime(date_str.strip(), '%Y%m%d')

# Function to read each CSV section
def read_csv_section(section_lines, start_date):
    # Use the first non-empty line as the header
    header_line = next(line for line in section_lines if line.strip())
    headers = header_line.split(',')
    
    # Create DataFrame from section lines, skipping the header
    data_lines = section_lines[section_lines.index(header_line) + 1:]
    df = pd.read_csv(StringIO('\n'.join(data_lines)), header=None)
    df.columns = headers

    # Convert 'Nth day' to actual dates if it's in the DataFrame
    if 'Nth day' in df.columns:
        df['Date'] = df['Nth day'].apply(lambda x: start_date + pd.Timedelta(days=int(x)))

    return df

# Function to process the CSV file
def process_csv_file(file_content):
    sections_data = {}
    lines = file_content.strip().split('\n')
    section_lines = []
    start_date = None

    for line in lines:
        if line.startswith('# Start date:'):
            # If there's an existing section, process it before starting a new one
            if section_lines:
                df = read_csv_section(section_lines, start_date)
                sections_data[section_name] = df
                section_lines = []  # Reset the section lines

            # Parse the start date for the new section
            start_date_str = line.split(': ')[1]
            start_date = parse_date(start_date_str)
        elif line.startswith('#'):
            # Skip all other metadata lines
            continue
        elif not line.strip():
            # Skip empty lines
            continue
        elif ',' in line:
            # This is a header or a data line
            if section_lines and not any(char.isdigit() for char in line):
                # If there are already lines captured and this line is a header (no digits), it starts a new section
                df = read_csv_section(section_lines, start_date)
                sections_data[section_name] = df
                section_lines = [line]  # Start new section with the header
            else:
                # Otherwise, it's part of the current section
                section_lines.append(line)
            section_name = line  # Update the current section name
        else:
            # It's a continuation of the data
            section_lines.append(line)

    # Process the last section after the loop ends
    if section_lines:
        df = read_csv_section(section_lines, start_date)
        sections_data[section_name] = df

    return sections_data

# File uploader in Streamlit
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
