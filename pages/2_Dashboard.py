import streamlit as st
import pandas as pd

# Create a Streamlit app
st.title("Google Search Console Data")

# Allow the user to upload multiple CSV files
uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

# Create an empty dataframe to store the combined data
combined_df = pd.DataFrame()

# Check if files have been uploaded
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Read each uploaded CSV file into a separate dataframe
        df = pd.read_csv(uploaded_file)
        
        # Append the data to the combined dataframe
        combined_df = combined_df.append(df, ignore_index=True)

    # Display the combined dataframe
    st.subheader("Combined Data")
    st.write(combined_df)

    # Create a chart using data from the combined dataframe
    st.subheader("Combined Chart")
    st.bar_chart(combined_df["Clicks"])
