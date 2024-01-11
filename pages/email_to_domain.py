import requests
from urllib.parse import urlparse

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

# Read the list of emails from a file
with open('emails.txt', 'r') as file:
    emails = file.read().splitlines()

# List to hold email and corresponding URL pairs
email_url_pairs = []

# Iterate over the emails and get the company URL
for email in emails:
    url = get_company_url(email)
    if url:
        email_url_pairs.append((email, url))

# Output the results in a table format
print("Email,Company URL")
for email, url in email_url_pairs:
    print(f"{email},{url}")
