import streamlit as st
import pandas as pd

# Create a Streamlit app
st.title("Google Search Console Data")

# Allow the user to upload a CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Display the DataFrame and visualizations
    st.subheader("Top Pages")
    st.table(df.head(10))  # Display the first 10 rows of the DataFrame
