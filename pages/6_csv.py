import os
import pandas as pd
import streamlit as st
import base64

def get_file_content_as_base64(path):
    """Encode file content to base64."""
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def process_xls(file):
    """Process each sheet in the xls file and save as individual CSV files."""
    # Load the Excel file
    xls = pd.ExcelFile(file, engine='xlrd')

    # Create a directory to store CSV files
    csv_dir = "csv_files"
    os.makedirs(csv_dir, exist_ok=True)

    # Process each sheet
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        csv_file = os.path.join(csv_dir, f"{sheet_name}.csv")
        df.to_csv(csv_file, index=False)
        st.success(f"CSV file saved: {csv_file}")

    return csv_dir

def main():
    """Main function for the Streamlit app."""
    st.title("XLS to CSV Converter")

    uploaded_file = st.file_uploader("Upload your XLS file", type=["xls"])

    if uploaded_file is not None:
        csv_dir = process_xls(uploaded_file)

        # Provide download links for the CSV files
        st.write("Download CSV Files:")
        csv_files = os.listdir(csv_dir)
        for file in csv_files:
            file_path = os.path.join(csv_dir, file)
            b64 = get_file_content_as_base64(file_path)
            href = f'<a href="data:file/csv;base64,{b64}" download="{file}">Download {file}</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
