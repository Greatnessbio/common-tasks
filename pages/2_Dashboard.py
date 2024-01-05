import streamlit as st
import pandas as pd

# Read the Google Search Console data into a DataFrame
df = pd.read_csv("google_search_console_data.csv")

# Create a tab for each of the metrics
st.title("Google Search Console Data")
st.subheader("Top Pages")
st.table(df[["Page", "Clicks", "Impressions", "CTR", "Position"]].head(10))

st.subheader("Clicks")
st.bar_chart(df["Clicks"])

st.subheader("Impressions")
st.line_chart(df["Impressions"])

st.subheader("CTR")
st.area_chart(df["CTR"])

st.subheader("Position")
st.scatter_plot(df["Position"], df["Impressions"])
