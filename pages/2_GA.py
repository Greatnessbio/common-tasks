import streamlit as st
import pandas as pd

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

if uploaded_file is not None:
    csv_content = uploaded_file.read().decode('utf-8')
    st.write(csv_content)
