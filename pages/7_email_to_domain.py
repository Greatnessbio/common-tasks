import requests
from urllib.parse import urlparse
import streamlit as st

# Function to get the company URL from an email domain
def get_company_url(email):
    domain = email.split('@')[-1]  # Extract the domain from the email
    try:
        response = requests.get(f"http://{domain}", timeout=5)
        if response.status_code == 200:
            return response.url
        else:
            return None
    except requests.RequestException:
        return None

# Streamlit UI
st.title("Email to Company URL Converter")

# Allow the user to upload a file
uploaded_file = st.file_uploader("Upload a file containing emails", type=["txt"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the list of emails from the uploaded file
    emails = uploaded_file.read().decode('utf-8').splitlines()

    # List to hold email and corresponding URL pairs
    email_url_pairs = []

    # Iterate over the emails and get the company URL
    for email in emails:
        url = get_company_url(email)
        if url:
            email_url_pairs.append((email, url))

    # Output the results in a table format
    st.write("Email, Company URL")
    for email, url in email_url_pairs:
        st.write(f"{email}, {url}")
