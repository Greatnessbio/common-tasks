import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load data from a CSV file and create a DataFrame
def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file, delimiter='\t', skiprows=11, nrows=28)
    df.columns = df.columns.str.strip()  # Clean column names
    return df

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Analysis")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    # Load data from the uploaded file
    df = load_data(uploaded_file)

    if df is not None:
        # Display the DataFrame
        st.write("Uploaded Data:")
        st.write(df)

        # Visualization options
        st.subheader("Data Visualization Options")

        if "Users" in df.columns and "Nth day" in df.columns:
            st.subheader("Line Chart - Users")
            plt.plot(df['Nth day'], df['Users'])
            plt.xlabel("Nth day")
            plt.ylabel("Users")
            st.pyplot()

        if "New users" in df.columns:
            st.subheader("Line Chart - New Users")
            plt.plot(df['Nth day'], df['New users'])
            plt.xlabel("Nth day")
            plt.ylabel("New Users")
            st.pyplot()

        if "First user default channel group" in df.columns:
            st.subheader("Bar Chart - First User Default Channel Group")
            df_bar = df.groupby('First user default channel group')['New users'].sum()
            st.bar_chart(df_bar)

        if "Session default channel group" in df.columns:
            st.subheader("Bar Chart - Session Default Channel Group")
            df_bar = df.groupby('Session default channel group')['Sessions'].sum()
            st.bar_chart(df_bar)

        if "Cohort" in df.columns and "LTV" in df.columns:
            st.subheader("Line Chart - Cohort LTV")
            plt.plot(df['Cohort'], df['LTV'])
            plt.xlabel("Cohort")
            plt.ylabel("LTV")
            st.pyplot()
