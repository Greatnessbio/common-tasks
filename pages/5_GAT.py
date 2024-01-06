import pandas as pd
import streamlit as st
from io import StringIO

def read_section(lines):
  if not lines:
    return pd.DataFrame()  # Return an empty DataFrame if section_lines is empty
  return pd.read_csv(StringIO(''.join(lines)), skipinitialspace=True)

# Rest of the code...
