import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d') if date_string is not None else None
    except ValueError:
        return None

def format_biorxiv_result(title, authors, pub_date_str, journal, doi_link, link):
    formatted_result = f"**[Title: {title}]({link})**\nAuthors: {authors}\nPublished in: {journal} on {pub_date_str}\nDOI: {doi_link}"
    return formatted_result

def format_pubmed_result(title, authors, pub_date_str, journal, doi_link, summary, link):
    formatted_result = f"**[Title: {title}]({link})**\nAuthors: {authors}\nPublished in: {journal} on {pub_date_str}\nDOI: {doi_link}\nSummary: {summary}"
    return formatted_result

def format_google_patents_link(query, link):
    formatted_result = f"Search for patents related to '{query}' on Google Patents: [View Results]({link})"
    return formatted_result

def search_biorxiv(query):
    formatted_query = query.replace(' ', '%20')
    url = f"https://www.biorxiv.org/search/{formatted_query}%20jcode%3Abiorxiv%7C%7Cmedrxiv%20numresults%3A50%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Astandard"
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
        journal = 'bioRxiv'
        doi_link = "https://doi.org/" + article.find('span', class_='highwire-cite-metadata-doi').get_text().strip() if article.find('span', class_='highwire-cite-metadata-doi') else None
        link = "https://www.biorxiv.org" + article.find('a', class_='highwire-cite-linked-title')['href']
        results.append((title, authors, pub_date_str, pub_date, summary, journal, doi_link, link))
    return results

def search_pubmed(query):
    formatted_query = query.replace(' ', '+')
    url = f"https://pubmed.ncbi.nlm.nih.gov/?term={formatted_query}&sort=date&size=20"
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
        journal = article.find('span', class_='docsum-journal-citation').get_text().strip().split('.')[1].strip() if article.find('span', class_='docsum-journal-citation') else None
        doi_link = f"https://doi.org/{article.find('span', class_='docsum-doi').get_text().strip()}" if article.find('span', class_='docsum-doi') else None
        link = "https://pubmed.ncbi.nlm.nih.gov" + article.find('a', class_='docsum-title')['href']
        results.append((title, authors, pub_date_str, pub_date, summary, journal, doi_link, link))
    return results

def google_patents_url(query):
    formatted_query = query.replace(' ', '+')
    return f"https://patents.google.com/?q=({formatted_query})&num=25&scholar&oq={formatted_query}&sort=new"

st.title("Literature Search App")

query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching bioRxiv..."):
            biorxiv_results = search_biorxiv(query)
            st.subheader("bioRxiv Results")
            for title, authors, pub_date_str, _, summary, journal, doi_link, link in biorxiv_results:
                formatted_result = format_biorxiv_result(title, authors, pub_date_str, journal, doi_link, link)
                st.markdown(formatted_result)

        with st.spinner("Searching PubMed..."):
            pubmed_results = search_pubmed(query)
            st.subheader("PubMed Results")
            for title, authors, pub_date_str, _, summary, journal, doi_link, link in pubmed_results:
                formatted_result = format_pubmed_result(title, authors, pub_date_str, journal, doi_link, summary, link)
                st.markdown(formatted_result)

        with st.spinner("Preparing Google Patents link..."):
            patents_link = google_patents_url(query)
            st.subheader("Google Patents Results")
            formatted_patents_link = format_google_patents_link(query, patents_link)
            st.markdown(formatted_patents_link)
    else:
        st.warning("Please enter a search query.")
