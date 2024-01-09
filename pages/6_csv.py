import streamlit as st
import pandas as pd
import os
from pathlib import Path
import base64

def process_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1]

    if file_extension.lower() == '.xlsx':
        xls = pd.read_excel(uploaded_file, sheet_name=None)
        sheet_names = list(xls.keys())
    elif file_extension.lower() == '.xls':
        # For '.xls' files, use an appropriate engine like 'xlrd' (version 1.2.0 or earlier)
        xls = pd.read_excel(uploaded_file, sheet_name=None, engine='xlrd') # Ensure you have the compatible version of xlrd
        sheet_names = list(xls.keys())
    else:
        st.error("Invalid file format. Please upload a valid Excel file.")
        return

    csv_folder = 'csv_files'
    os.makedirs(csv_folder, exist_ok=True)

    for sheet_name, df in xls.items():
        csv_filename = f"{csv_folder}/{sheet_name}.csv"
        df.to_csv(csv_filename, index=False)

    st.success(f"CSV files saved in folder: {csv_folder}")

def main():
    st.title("Excel to CSV Converter")

    # File uploader that accepts both .xlsx and .xls files
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])

    if uploaded_file is not None:
        process_file(uploaded_file)

        # Provide a download link for the CSV files
        csv_folder = 'csv_files'
        csv_files = os.listdir(csv_folder)
        if csv_files:
            with st.expander("Download CSV Files"):
                for csv_file in csv_files:
                    csv_path = os.path.join(csv_folder, csv_file)
                    if "[" in csv_file and "]" in csv_file:
                        csv_file_name = csv_file.split("[")[1].split("]")[0]
                    else:
                        csv_file_name = csv_file
                    st.markdown(f"[{csv_file_name}]({csv_path})")

            # Add a download all button
            csv_files_paths = [os.path.join(csv_folder, csv_file) for csv_file in csv_files]
            all_csv_zip = 'all_csv_files.zip'
            Path(all_csv_zip).unlink(missing_ok=True)  # Remove existing zip file if it exists

            # Create a zip file containing all CSV files
            os.system(f'zip -j {all_csv_zip} {" ".join(csv_files_paths)}')

            # Provide a download link for the zip file
            with open(all_csv_zip, "rb") as f:
                zip_file_content = f.read()
            st.download_button(
                label="Download All CSV Files as ZIP",
                data=zip_file_content,
                file_name=all_csv_zip,
                key="download_zip_button",
            )

if __name__ == "__main__":
    main()
