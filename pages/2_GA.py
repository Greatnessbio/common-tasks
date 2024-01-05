import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load and process the data
def load_data(uploaded_file):
    # Read the CSV file
    df = pd.read_csv(uploaded_file)

    # Split the dataframe into different datasets based on your CSV structure
    users_data = df.iloc[:28, :2]
    new_users_data = df.iloc[30:58, :2]
    channel_group_data = df.iloc[60:68, :2]
    session_channel_data = df.iloc[70:78, :2]

    return users_data, new_users_data, channel_group_data, session_channel_data

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

    # Visualization for Daily Users and New Users Data
    st.subheader("Daily Users and New Users Trend")
    plot_users_graph(users_data, new_users_data)

    # Visualization for First User Default Channel Group
    st.subheader("First User Default Channel Distribution")
    plot_channel_distribution(channel_group_data, "New Users per Channel")

    # Visualization for Session Default Channel Group
    st.subheader("Session Default Channel Distribution")
    plot_channel_distribution(session_channel_data, "Sessions per Channel")

else:
    st.write("Upload a CSV file to see the visualizations.")
