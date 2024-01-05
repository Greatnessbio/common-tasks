import pandas as pd
import streamlit as st

# Load the entire CSV file
df = pd.read_csv('your_file.csv', header=None)

# Initialize an empty dictionary to hold your datasets
datasets = {}

# Initialize variables to hold the current dataset and column names
current_dataset = None
column_names = None

# Iterate over the DataFrame by row
for idx, row in df.iterrows():
    # If this row contains metadata (identified by checking if the first cell starts with '#')
    if str(row[0]).startswith('#'):
        # This row is metadata, so update the current dataset and column names
        current_dataset = row[0]
        column_names = [row[0], row[1]]
        # Create a new DataFrame for this dataset
        datasets[current_dataset] = pd.DataFrame(columns=column_names)
    elif current_dataset is not None:
        # This row is data, so add it to the current dataset
        datasets[current_dataset] = datasets[current_dataset].append(pd.Series(row.values, index=column_names), ignore_index=True)

# Now, 'datasets' is a dictionary that maps metadata to DataFrames

# Use Streamlit to display the datasets
for metadata, dataset in datasets.items():
    st.write(f"Dataset for {metadata}:")
    st.dataframe(dataset)
