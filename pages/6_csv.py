import streamlit as st
import pandas as pd
import os

def process_file(uploaded_file):
    file_extension = os.path.splitext(uploaded_file.name)[1]

    if file_extension.lower() == '.xlsx':
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names
    elif file_extension.lower() == '.xls':
        # For '.xls' files, use an appropriate engine like 'xlrd' (version 1.2.0 or earlier)
        xls = pd.read_excel(uploaded_file, engine='xlrd') # Ensure you have the compatible version of xlrd
        sheet_names = xls.sheet_names
    else:
        st.error("Invalid file format. Please upload a valid Excel file.")
        return

    csv_folder = 'csv_files'
    os.makedirs(csv_folder, exist_ok=True)

    for sheet_name in sheet_names:
        df = xls.parse(sheet_name)
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
            with st.beta_expander("Download CSV Files"):
                for csv_file in csv_files:
                    csv_path = os.path.join(csv_folder, csv_file)
                    st.markdown(f"[{csv_file}]({csv_path})")

if __name__ == "__main__":
    main()
