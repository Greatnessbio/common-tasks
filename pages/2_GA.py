import streamlit as st
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

def read_csv_sections(csv_content):
    sections = []
    lines = csv_content.strip().split('\n')

    # Extract start and end dates from metadata
    start_date_str = next((line.split(': ')[-1].strip() for line in lines if line.startswith('Start date:')), None)
    end_date_str = next((line.split(': ')[-1].strip() for line in lines if line.startswith('End date:')), None)

    if not start_date_str or not end_date_str:
        raise ValueError("Start date or end date not found in the file.")

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

    # Define the section headers
    section_headers = [
        "Nth day\tUsers",
        "Nth day\tNew users",
        "First user default channel group\tNew users",
        "Session default channel group\tSessions",
        "Session Google Ads campaign\tSessions",
        "Cohort\tLTV"
    ]

    # Find lines where new sections start
    start_indices = [i for i, line in enumerate(lines) if any(header in line for header in section_headers)]
    start_indices.append(len(lines))  # Add end of file as the last index

    # Iterate over each section
    for i in range(len(start_indices) - 1):
        start_index = start_indices[i]
        end_index = start_indices[i + 1] - 1  # Adjust for section header
        section_lines = lines[start_index+1:end_index]  # Skip the header line

        # Extract the section name
        section_name = lines[start_index]

        # Convert 'Nth day' to actual dates
        section_df = pd.read_csv(StringIO('\n'.join(section_lines)), delimiter='\t', header=None)
        section_df.columns = ['Nth day', 'Value']
        section_df['Date'] = section_df['Nth day'].apply(lambda x: start_date + timedelta(days=int(x)-1))

        # Add the section to the list
        sections.append((section_name, section_df))

    return sections, start_date_str, end_date_str

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    try:
        csv_content = uploaded_file.read().decode('utf-8')
        sections, start_date, end_date = read_csv_sections(csv_content)
        
        st.write(f"Start Date: {start_date}")
        st.write(f"End Date: {end_date}")

        # Render each section's DataFrame using Streamlit
        for section_name, section_df in sections:
            st.subheader(section_name)
            st.write(section_df)
    except Exception as e:
        st.error(f"Error processing file: {e}")
else:
    st.info("Please upload a CSV file.")
