import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime

def read_csv_section(section_lines):
    # Parse metadata for start and end dates
    metadata_lines = [line for line in section_lines if line.startswith('#')]
    metadata = {line.split(': ')[0].strip('# '): line.split(': ')[1] for line in metadata_lines}
    start_date = datetime.strptime(metadata['Start date'], '%Y%m%d')  # Ensure the format matches 'YYYYMMDD'
    
    # Filter out metadata and empty lines
    section_content = [line for line in section_lines if not line.startswith('#') and line.strip()]
    
    # Check if there is content to create a DataFrame
    if section_content:
        # Assume the second line is the header, based on the provided file structure
        header = section_content[0]
        data_lines = section_content[1:]
        
        # Create DataFrame from section lines
        df = pd.read_csv(StringIO('\n'.join(data_lines)), sep='\t', header=None, names=header.split('\t'))
        
        # Convert 'Nth day' to actual dates if it's in the DataFrame
        if 'Nth day' in df.columns:
            df['Date'] = df['Nth day'].apply(lambda x: start_date + pd.Timedelta(days=int(x)))
    else:
        df = pd.DataFrame()

    return df, metadata

def process_csv_file(file_content):
    sections_data = {}
    lines = file_content.strip().split('\n')
    section_starts = [i for i, line in enumerate(lines) if line.startswith('# Start date:')]

    # Add end of file as the last index for the last section
    section_starts.append(len(lines))

    for i in range(len(section_starts) - 1):
        start_idx = section_starts[i]
        end_idx = section_starts[i + 1]
        section_name = lines[start_idx + 1].strip()
        
        if section_name:
            df, metadata = read_csv_section(lines[start_idx:end_idx])
            sections_data[section_name] = {'DataFrame': df, 'Metadata': metadata}

    return sections_data

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        file_content = uploaded_file.read().decode('utf-8')
        sections_data = process_csv_file(file_content)

        for section_name, data in sections_data.items():
            st.write(f"Section: {section_name}")
            st.write(f"Metadata: {data['Metadata']}")
            st.dataframe(data['DataFrame'])

    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file.")
