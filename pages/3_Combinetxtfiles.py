import os
import re
import streamlit as st

def combine_txt_files(folder_path):
    # List to hold the contents of all text files
    all_texts = []

    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)

            # Open and read the text file
            with open(file_path, 'r') as file:
                file_content = file.read().strip()
                # Add filename and file content to the list, followed by an empty line
                all_texts.append(f"File: {filename}\n{file_content}\n")

    # Combine all texts
    combined_text = "\n".join(all_texts)

    return combined_text

# Streamlit UI
st.title("Combine Text Files")

# Allow user to select a folder
folder_path = st.file_uploader("Select a folder containing .txt files", type="folder")
output_file = None

if folder_path:
    # Display a button to trigger the combination and download
    if st.button("Combine and Download"):
        combined_text = combine_txt_files(folder_path)
        output_file = 'combined.txt'

# Download button
if output_file:
    with open(output_file, 'w') as file:
        file.write(combined_text)
    st.download_button("Download Combined Text", output_file)
