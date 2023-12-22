import streamlit as st
import requests
from bs4 import BeautifulSoup

def search_biorxiv(query):
    url = f"https://www.biorxiv.org/search/{query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('li', class_='search-result')
    results = []
    for article in articles:
        title = article.find('span', class_='highwire-cite-title').get_text()
        summary = article.find('div', class_='highwire-cite-snippet').get_text().strip() if article.find('div', class_='highwire-cite-snippet') else 'No summary available'
        link = "https://www.biorxiv.org" + article.find('a', class_='highwire-cite-linked-title')['href']
        results.append((title, summary, link))
    return results

def search_pubmed(query):
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('article', class_='full-docsum')
    results = []
    for article in articles:
        title = article.find('a', class_='docsum-title').get_text().strip()
        summary = article.find('div', class_='full-view-snippet').get_text().strip() if article.find('div', class_='full-view-snippet') else 'No summary available'
        link = "https://pubmed.ncbi.nlm.nih.gov" + article.find('a', class_='docsum-title')['href']
        results.append((title, summary, link))
    return results

st.title("Literature Search App")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching bioRxiv..."):
            biorxiv_results = search_biorxiv(query)
            st.subheader("bioRxiv Results")
            for title, summary, link in biorxiv_results:
                st.markdown(f"**[{title}]({link})**")
                st.write(summary)

        with st.spinner("Searching PubMed..."):
            pubmed_results = search_pubmed(query)
            st.subheader("PubMed Results")
            for title, summary, link in pubmed_results:
                st.markdown(f"**[{title}]({link})**")
                st.write(summary)
    else:
        st.warning("Please enter a search query.")
