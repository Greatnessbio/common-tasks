import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Function to load and preprocess a specific section of the data
def load_data_section(uploaded_file, section_name):
    df = pd.read_csv(uploaded_file, delimiter='\t', skiprows=11, nrows=28)

    # Clean column names by stripping leading and trailing whitespace
    df.columns = df.columns.str.strip()

    return df

# Streamlit app layout
st.title("Google Analytics Acquisitions Data Analysis")

# Create an upload file widget
uploaded_file = st.file_uploader("Upload the Google Analytics CSV file", type=["csv"])

if uploaded_file is not None:
    data_sections = {
        "Users": load_data_section(uploaded_file, "Nth day Users"),
        "New Users": load_data_section(uploaded_file, "Nth day New users"),
        "First User Default Channel Group": load_data_section(uploaded_file, "First user default channel group New users"),
        "Session Default Channel Group": load_data_section(uploaded_file, "Session default channel group Sessions"),
        "Session Google Ads Campaign": load_data_section(uploaded_file, "Session Google Ads campaign Sessions"),
        "Cohort LTV": load_data_section(uploaded_file, "Cohort LTV")
    }

    # Allow users to select a data section
    selected_section = st.selectbox("Select a data section", list(data_sections.keys()))

    # Display the selected DataFrame
    st.write(f"Selected Data Section: {selected_section}")
    st.write(data_sections[selected_section])

    # Create visualizations based on the selected section
    if selected_section in ["Users", "New Users"]:
        st.subheader("Line Chart")
        plt.plot(data_sections[selected_section]['Nth day'], data_sections[selected_section][selected_section])
        plt.xlabel("Nth day")
        plt.ylabel(selected_section)
        st.pyplot()

    elif selected_section == "First User Default Channel Group":
        st.subheader("Bar Chart")
        df_bar = data_sections[selected_section].groupby('First user default channel group')['New users'].sum()
        st.bar_chart(df_bar)
