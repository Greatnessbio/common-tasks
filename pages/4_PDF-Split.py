import PyPDF2
import streamlit as st
import io
import zipfile

# Function to add PDF chunks to a zip file
def add_to_zip(zip_file, pdf_chunks):
    for i, chunk in enumerate(pdf_chunks, start=1):
        chunk.seek(0)
        zip_file.writestr(f"chunk_{i}.pdf", chunk.read())

# Set the title and description for your Streamlit app
st.title("PDF Splitter")
st.write("This app allows you to split a PDF into smaller chunks.")

# Upload a PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Get the maximum chunk size from the user
    max_chunk_size = st.number_input("Maximum Chunk Size (MB)", min_value=1, value=100)

    if st.button("Split PDF"):
        # Initialize session state for PDF chunks
        if 'pdf_chunks' not in st.session_state:
            st.session_state['pdf_chunks'] = []

        # Open the uploaded PDF file
        with pdf_file as file:
            reader = PyPDF2.PdfReader(file)

            # Initialize variables for chunking
            current_chunk_size = 0
            writer = PyPDF2.PdfWriter()

            # Iterate over each page in the PDF
            for page in reader.pages:
                # Use in-memory buffer for temporary storage
                temp_buffer = io.BytesIO()
                temp_writer = PyPDF2.PdfWriter()
                temp_writer.add_page(page)
                temp_writer.write(temp_buffer)
                temp_file_size = temp_buffer.tell()

                # Check chunk size
                if current_chunk_size + temp_file_size > max_chunk_size * 1024 * 1024:
                    chunk_buffer = io.BytesIO()
                    writer.write(chunk_buffer)
                    st.session_state['pdf_chunks'].append(chunk_buffer.getvalue())
                    current_chunk_size = 0
                    writer = PyPDF2.PdfWriter()

                writer.add_page(page)
                current_chunk_size += temp_file_size

            if current_chunk_size > 0:
                chunk_buffer = io.BytesIO()
                writer.write(chunk_buffer)
                st.session_state['pdf_chunks'].append(chunk_buffer.getvalue())

        st.success("PDF split into smaller chunks.")

    # Create a single download button for all chunks
    if 'pdf_chunks' in st.session_state and st.session_state['pdf_chunks']:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            add_to_zip(zip_file, st.session_state['pdf_chunks'])
        zip_buffer.seek(0)
        st.download_button("Download All Chunks", zip_buffer, file_name="pdf_chunks.zip", mime="application/zip")
