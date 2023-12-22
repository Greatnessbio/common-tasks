import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def parse_date(date_string):
    # Adjust this function based on the date format of the website
    try:
        return datetime.strptime(date_string, '%d %b %Y')
    except ValueError:
        return None

def search_biorxiv(query):
    url = f"https://www.biorxiv.org/search/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('li', class_='search-result')
    results = []
    for article in articles:
        title = article.find('span', class_='highwire-cite-title').get_text()
        summary = article.find('div', class_='highwire-cite-snippet').get_text().strip() if article.find('div', class_='highwire-cite-snippet') else 'No summary available'
        authors = article.find('span', class_='highwire-citation-authors').get_text().strip() if article.find('span', class_='highwire-citation-authors') else 'No authors listed'
        pub_date_str = article.find('span', class_='highwire-cite-metadata-date').get_text().strip() if article.find('span', class_='highwire-cite-metadata-date') else None
        pub_date = parse_date(pub_date_str)
        journal = 'bioRxiv'  # Since the source is bioRxiv
        doi_link = "https://doi.org/" + article.find('span', class_='highwire-cite-metadata-doi').get_text().strip() if article.find('span', class_='highwire-cite-metadata-doi') else None
        link = "https://www.biorxiv.org" + article.find('a', class_='highwire-cite-linked-title')['href']
        results.append((title, authors, pub_date_str, pub_date, summary, journal, doi_link, link))
    return sorted(results, key=lambda x: x[3], reverse=True)  # Sort by publication date

def search_pubmed(query):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='full-docsum')
    results = []
    for article in articles:
        title = article.find('a', class_='docsum-title').get_text().strip()
        summary = article.find('div', class_='full-view-snippet').get_text().strip() if article.find('div', class_='full-view-snippet') else 'No summary available'
        authors = article.find('span', class_='docsum-authors').get_text().strip() if article.find('span', class_='docsum-authors') else 'No authors listed'
        pub_date_str = article.find('span', class_='docsum-journal-citation').get_text().strip().split('.')[0] if article.find('span', class_='docsum-journal-citation') else None
        pub_date = parse_date(pub_date_str)
        journal = re.search(r'\. (\w+[\w\s]+)\.', article.find('span', class_='docsum-journal-citation').get_text().strip()).group(1) if article.find('span', class_='docsum-journal-citation') else None
        doi = article.find('span', class_='docsum-doi').get_text().strip() if article.find('span', class_='docsum-doi') else None
        doi_link = f"https://doi.org/{doi}" if doi else None
        link = "https://pubmed.ncbi.nlm.nih.gov" + article.find('a', class_='docsum-title')['href']
        results.append((title, authors, pub_date_str, pub_date, summary, journal, doi_link, link))
    return sorted(results, key=lambda x: x[3], reverse=True)  # Sort by publication date

st.title("Literature Search App")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching bioRxiv..."):
            biorxiv_results = search_biorxiv(query)
            st.subheader("bioRxiv Results")
            for title, authors, pub_date_str, _, summary, journal, doi_link, link in biorxiv_results:
                st.markdown(f"**[{title}]({link})**")
                st.write(f"Authors: {authors}")
                st.write(f"Published on: {pub_date_str}")
                st.write(f"Journal: {journal}")
                st.markdown(f"DOI: [{doi_link}]({doi_link})") if doi_link else st.write("DOI: Not available")
                st.write(f"Summary: {summary}")

        with st.spinner("Searching PubMed..."):
            pubmed_results = search_pubmed(query)
            st.subheader("PubMed Results")
            for title, authors, pub_date_str, _, summary, journal, doi_link, link in pubmed_results:
                st.markdown(f"**[{title}]({link})**")
                st.write(f"Authors: {authors}")
                st.write(f"Published on: {pub_date_str}")
                st.write(f"Journal: {journal}")
                st.markdown(f"DOI: [{doi_link}]({doi_link})") if doi_link else st.write("DOI: Not available")
                st.write(f"Summary: {summary}")
    else:
        st.warning("Please enter a search query.")
