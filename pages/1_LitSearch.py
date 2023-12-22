import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%d %b %Y') if date_string is not None else None
    except ValueError:
        return None

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
        journal = 'bioRxiv'  # Since the source is bioRxiv
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
        pub_date_str = article.find('span', class='docsum-journal-citation').get_text().strip().split('.')[0] if article.find('span', class='docsum-journal-citation') else None
        pub_date = parse_date(pub_date_str)
        journal = article.find('span', class='docsum-journal-citation').get_text().strip().split('.')[1].strip() if article.find('span', class='docsum-journal-citation') else None
        doi_link = f"https://doi.org/{article.find('span', class='docsum-doi').get_text().strip()}" if article.find('span', class='docsum-doi') else None
        link = "https://pubmed.ncbi.nlm.nih.gov" + article.find('a', class='docsum-title')['href']
        results.append((title, authors, pub_date_str, pub_date, summary, journal, doi_link, link))
    return results

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
                if doi_link:
                    st.markdown(f"DOI: [{doi_link}]({doi_link})")
                else:
                    st.write("DOI: Not available")
                st.write(f"Summary: {summary}")

        with st.spinner("Searching PubMed..."):
            pubmed_results = search_pubmed(query)
            st.subheader("PubMed Results")
            for title, authors, pub_date_str, _, summary, journal, doi_link, link in pubmed_results:
                st.markdown(f"**[{title}]({link})**")
                st.write(f"Authors: {authors}")
                st.write(f"Published on: {pub_date_str}")
                st.write(f"Journal: {journal}")
                if doi_link:
                    st.markdown(f"DOI: [{doi_link}]({doi_link})")
                else:
                    st.write("DOI: Not available")
                st.write(f"Summary: {summary}")
    else:
        st.warning("Please enter a search query.")
