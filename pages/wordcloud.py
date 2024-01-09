import streamlit as st
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np

# Define predefined color schemes
color_schemes = {
    "Default": "viridis",
    "Blue": "Blues",
    "Red": "Reds",
    "Green": "Greens",
    "Purple": "Purples",
}

# Streamlit UI
st.title("Scientific Paper Word Cloud Generator")

# Text area for pasting paragraphs
text = st.text_area("Paste your paragraphs here:")

# Checkbox to remove stop words
remove_stopwords = st.checkbox("Remove Stop Words")

# Select color scheme
selected_color_scheme = st.selectbox("Select Color Scheme:", list(color_schemes.keys()))

# Generate word cloud
if st.button("Generate Word Cloud"):
    if text:
        # Create a WordCloud object
        wordcloud = WordCloud(
            background_color="white",
            width=800,
            height=400,
            colormap=color_schemes[selected_color_scheme],
            stopwords=STOPWORDS if remove_stopwords else None,
        )

        # Generate the word cloud
        wordcloud.generate(text)

        # Display the word cloud using matplotlib
        st.pyplot(plt.figure(figsize=(10, 5)))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

    else:
        st.warning("Please enter some text to generate a word cloud.")

# Information and tips
st.markdown("### Tips:")
st.write("- Paste your paragraphs into the text area.")
st.write("- You can choose to remove stop words to filter common words.")
st.write("- Select a color scheme for the word cloud.")

# Footer
st.markdown("---")
st.write("Created by Your Name")

