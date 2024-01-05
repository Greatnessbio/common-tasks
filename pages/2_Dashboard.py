import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and preprocess the data
def load_data(uploaded_file):
    # Read the uploaded CSV file into a DataFrame
    df = pd.read_csv(uploaded_file, delimiter='\t', skiprows=11, nrows=28)
    return df

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Analysis")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    df = load_data(uploaded_file)

    # Display the DataFrame
    st.write("Uploaded Data:")
    st.write(df)

    # Create visualizations
    st.subheader("Line Chart - Users")
    plt.plot(df['Nth day'], df['Users'])
    plt.xlabel("Nth day")
    plt.ylabel("Users")
    st.pyplot()

    st.subheader("Line Chart - New Users")
    plt.plot(df['Nth day'], df['New users'])
    plt.xlabel("Nth day")
    plt.ylabel("New Users")
    st.pyplot()

    st.subheader("Bar Chart - First user default channel group")
    df_bar = df.groupby('First user default channel group')['New users'].sum()
    st.bar_chart(df_bar)
