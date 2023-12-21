import PyPDF2
import streamlit as st
import io

# Set the title and description for your Streamlit app
st.title("PDF Splitter")
st.write("This app allows you to split a PDF into smaller chunks.")

# Upload a PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Get the maximum chunk size from the user
    max_chunk_size = st.number_input("Maximum Chunk Size (MB)", min_value=1, value=100)

    if st.button("Split PDF"):
        # Open the uploaded PDF file
        with pdf_file as file:
            reader = PyPDF2.PdfReader(file)

            # Initialize variables to keep track of the current chunk size and the pages in the chunk
            current_chunk_size = 0
            chunk_number = 1
            writer = PyPDF2.PdfWriter()

            # Buffer to store PDF chunks
            pdf_chunks = []

            # Iterate over each page in the PDF
            for page_num, page in enumerate(reader.pages):
                # Use in-memory buffer
                temp_buffer = io.BytesIO()
                temp_writer = PyPDF2.PdfWriter()
                temp_writer.add_page(page)
                temp_writer.write(temp_buffer)

                # Get the size of the buffer
                temp_file_size = temp_buffer.tell()

                # Check if adding the current page would exceed the maximum chunk size
                if current_chunk_size + temp_file_size > max_chunk_size * 1024 * 1024:
                    # Save the current chunk to buffer
                    chunk_buffer = io.BytesIO()
                    writer.write(chunk_buffer)
                    pdf_chunks.append(chunk_buffer)

                    # Reset the variables for the new chunk
                    current_chunk_size = 0
                    chunk_number += 1
                    writer = PyPDF2.PdfWriter()

                # Add the current page to the current chunk
                writer.add_page(page)
                current_chunk_size += temp_file_size

            # Create the last chunk if there are remaining pages
            if current_chunk_size > 0:
                chunk_buffer = io.BytesIO()
                writer.write(chunk_buffer)
                pdf_chunks.append(chunk_buffer)

            # Provide a download button for the generated chunks
            st.success("PDF split into smaller chunks.")
            st.write("Download the split chunks:")
            for i, chunk in enumerate(pdf_chunks, start=1):
                chunk.seek(0)
                st.download_button(f"Download Chunk {i}", chunk, file_name=f"chunk_{i}.pdf", mime="application/octet-stream")
