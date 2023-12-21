# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import PyPDF2
import os
import streamlit as st
import base64

# Set the title and description for your Streamlit app
st.title("PDF Splitter")
st.write("This app allows you to split a PDF into smaller chunks.")

# Upload a PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Get the maximum chunk size from the user
    max_chunk_size = st.number_input("Maximum Chunk Size (MB)", min_value=1, value=100)

    if st.button("Split PDF"):
        # Create a directory to store the split chunks
        output_directory = 'output/'
        os.makedirs(output_directory, exist_ok=True)

        # Open the uploaded PDF file
        with pdf_file as file:
            reader = PyPDF2.PdfReader(file)

            # Initialize variables to keep track of the current chunk size and the pages in the chunk
            current_chunk_size = 0
            chunk_number = 1
            writer = PyPDF2.PdfWriter()

            # Iterate over each page in the PDF
            for page_num, page in enumerate(reader.pages):
                # Create a temporary PDF file to estimate the page size
                temp_pdf_path = '/tmp/temp.pdf'
                temp_writer = PyPDF2.PdfWriter()
                temp_writer.add_page(page)

                # Save the temporary PDF file
                with open(temp_pdf_path, 'wb') as temp_file:
                    temp_writer.write(temp_file)

                # Get the size of the temporary PDF file
                temp_file_size = os.path.getsize(temp_pdf_path)

                # Check if adding the current page would exceed the maximum chunk size
                if current_chunk_size + temp_file_size > max_chunk_size * 1024 * 1024:
                    # Generate the output file path for the current chunk
                    output_file = os.path.join(output_directory, f'chunk_{chunk_number}.pdf')

                    # Write the current chunk to the output file
                    with open(output_file, 'wb') as output:
                        writer.write(output)

                    # Reset the variables for the new chunk
                    current_chunk_size = 0
                    chunk_number += 1
                    writer = PyPDF2.PdfWriter()

                # Add the current page to the current chunk
                writer.add_page(page)
                current_chunk_size += temp_file_size

            # Create the last chunk if there are remaining pages
            if current_chunk_size > 0:
                # Generate the output file path for the last chunk
                output_file = os.path.join(output_directory, f'chunk_{chunk_number}.pdf')

                # Write the last chunk to the output file
                with open(output_file, 'wb') as output:
                    writer.write(output)

        # Provide download links for the generated chunks
        st.success("PDF split into smaller chunks.")
        st.write("Download the split chunks:")
        for i in range(1, chunk_number + 1):
            chunk_path = os.path.join(output_directory, f'chunk_{i}.pdf')
            with open(chunk_path, 'rb') as file:
                # Read the file contents
                pdf_contents = file.read()
                # Encode the file contents in base64
                pdf_base64 = base64.b64encode(pdf_contents).decode('utf-8')
                # Create a download link for the PDF chunk
                st.markdown(f'<a href="data:application/pdf;base64,{pdf_base64}" download="chunk_{i}.pdf">Chunk {i}</a>', unsafe_allow_html=True)
