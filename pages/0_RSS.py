import streamlit as st
import feedparser

def display_rss_feed(feed_url):
    feed = feedparser.parse(feed_url)
    for entry in feed.entries:
        st.write(f"Title: {entry.title}")
        st.write(f"Link: {entry.link}")
        st.write(f"Published: {entry.published}")
        st.write(f"Summary: {entry.summary}")
        st.write("---")

def main():
    st.title("RSS Feed Display")
    feed_url = st.text_input("Enter RSS feed URL")

    if st.button("Display Feed"):
        if feed_url:
            display_rss_feed(feed_url)
        else:
            st.write("Please enter an RSS feed URL.")

if __name__ == "__main__":
    main()
