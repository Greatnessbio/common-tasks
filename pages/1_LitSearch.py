import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_biorxiv(query):
    url = f"https://www.biorxiv.org/search/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('span', class_='highwire-cite-title')
    return [article.get_text() for article in articles]

def search_pubmed(query):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('a', class_='docsum-title')
    return [article.get_text().strip() for article in articles]

st.title("Literature Search App")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching bioRxiv..."):
            biorxiv_results = search_biorxiv(query)
            st.subheader("bioRxiv Results")
            for result in biorxiv_results:
                st.write(result)

        with st.spinner("Searching PubMed..."):
            pubmed_results = search_pubmed(query)
            st.subheader("PubMed Results")
            for result in pubmed_results:
                st.write(result)
    else:
        st.warning("Please enter a search query.")
