import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load and process the data
def load_data(uploaded_file):
    try:
        # Read the entire file into a string
        file_content = uploaded_file.read().decode("utf-8")
        
        # Split the file content by the section headers
        sections = file_content.split('# ----------------------------------------')
        
        # Parse each section separately
        users_data = pd.read_csv(pd.compat.StringIO(sections[1]), skiprows=4, nrows=28)
        new_users_data = pd.read_csv(pd.compat.StringIO(sections[2]), skiprows=3, nrows=28)
        channel_group_data = pd.read_csv(pd.compat.StringIO(sections[3]), skiprows=3, nrows=8)
        session_channel_data = pd.read_csv(pd.compat.StringIO(sections[4]), skiprows=3, nrows=8)

        return users_data, new_users_data, channel_group_data, session_channel_data

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None

# Function to plot the users and new users graph
def plot_users_graph(users_data, new_users_data):
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=users_data, x='Nth day', y='Users', label='Users')
    sns.lineplot(data=new_users_data, x='Nth day', y='New users', label='New Users')
    plt.title('Daily Users and New Users Trend')
    plt.xlabel('Nth Day')
    plt.ylabel('Count')
    st.pyplot(plt)

# Function to plot the channel distribution
def plot_channel_distribution(data, title):
    plt.figure(figsize=(10, 5))
    sns.barplot(data=data, x=data.columns[1], y=data.columns[0])
    plt.title(title)
    plt.xlabel('Count')
    plt.ylabel(data.columns[0])
    st.pyplot(plt)

# Streamlit app main body
st.title('KPI Data Visualizer')

uploaded_file = st.file_uploader("Upload CSV", type="csv")
if uploaded_file:
    users_data, new_users_data, channel_group_data, session_channel_data = load_data(uploaded_file)

    if users_data is not None and new_users_data is not None:
        # Visualization for Daily Users and New Users Data
        st.subheader("Daily Users and New Users Trend")
        plot_users_graph(users_data, new_users_data)

    if channel_group_data is not None:
        # Visualization for First User Default Channel Group
        st.subheader("First User Default Channel Distribution")
        plot_channel_distribution(channel_group_data, "New Users per Channel")

    if session_channel_data is not None:
        # Visualization for Session Default Channel Group
        st.subheader("Session Default Channel Distribution")
        plot_channel_distribution(session_channel_data, "Sessions per Channel")

else:
    st.write("Upload a CSV file to see the visualizations.")
