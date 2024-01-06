import pandas as pd
import streamlit as st
from io import StringIO

def read_section(lines):
  return pd.read_csv(StringIO(''.join(lines)), skipinitialspace=True)

# Upload the CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file is not None:
  # Read the entire CSV file
  file_content = uploaded_file.getvalue().decode().splitlines()

  # Create a dictionary of DataFrames
  dfs = {}
  i = 0
  while i < len(file_content):
    line = file_content[i]
    if line.startswith('Nth day') or line.startswith('First user default channel group') or line.startswith('Session default channel group') or line.startswith('Session Google Ads campaign') or line.startswith('Cohort'):
      section_lines = []
      i += 1
      while i < len(file_content) and file_content[i].strip() != '':
        section_lines.append(file_content[i])
        i += 1
      df = read_section(section_lines)
      dfs[line.strip()] = df
    else:
      i += 1

  # Display the DataFrames
  for header, df in dfs.items():
    st.write(f"DataFrame for {header}:")
    st.dataframe(df)
