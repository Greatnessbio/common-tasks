import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from io import StringIO
from tempfile import mkdtemp

# Create a temporary directory to save uploaded files
temp_dir = mkdtemp()

# Save uploaded files to a temporary directory and return DataFrame
def save_and_load_uploaded_files(uploaded_files):
    dataframes = {}
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            bytes_data = uploaded_file.read()
            df = pd.read_csv(StringIO(bytes_data.decode('utf-8')))
            dataframes[uploaded_file.name] = df
            with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
                f.write(bytes_data)
    return dataframes

# Function to plot data
def plot_data(df, x, y, kind="bar"):
    fig, ax = plt.subplots()
    if kind == "bar":
        sns.barplot(data=df, x=x, y=y, ax=ax)
    elif kind == "line":
        sns.lineplot(data=df, x=x, y=y, ax=ax)
    elif kind == "area":
        df.plot(kind='area', x=x, y=y, ax=ax)
    elif kind == "pie":
        df.plot(kind='pie', y=y, labels=df[x], ax=ax)
    st.pyplot(fig)

# Streamlit application layout
def main():
    st.title("GSC Data Visualization App")
    
    # File Upload Interface
    uploaded_files = st.file_uploader("Upload CSV", type=['csv'], accept_multiple_files=True)
    
    if uploaded_files:
        dataframes = save_and_load_uploaded_files(uploaded_files)
        
        # Data Visualization
        st.header("Data Visualization")
        plot_type = st.selectbox("Select the type of plot", ["bar", "line", "area", "pie"])
        df_names = list(dataframes.keys())
        df_to_plot = st.selectbox("Select the DataFrame", df_names)
        
        if df_to_plot:
            df = dataframes[df_to_plot]
            if plot_type != "pie":  # Pie chart requires only y-axis
                x_axis = st.selectbox("Select x-axis", df.columns)
            y_axis = st.selectbox("Select y-axis", df.columns)
            
            # Button to plot
            if st.button("Plot"):
                plot_data(df, x_axis, y_axis, plot_type)
        
        # Data Combination Logic (optional, depending on user's need)
        # Example combining two dataframes by a common column
        st.header("Data Combination")
        df1_key = st.selectbox("Select first DataFrame for combination", df_names, key='df1')
        df2_key = st.selectbox("Select second DataFrame for combination", df_names, key='df2')
        common_column = st.text_input("Enter the common column name to combine on")
        
        if st.button("Combine and Plot"):
            if df1_key and df2_key and common_column:
                combined_df = pd.merge(dataframes[df1_key], dataframes[df2_key], on=common_column, how='inner')
                st.write(combined_df)
                # After displaying the combined dataframe, users can decide how to visualize it.
            else:
                st.error("Please select both dataframes and specify the common column.")

if __name__ == "__main__":
    main()
