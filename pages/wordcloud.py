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
    "Cool": "cool",
    "Spectral": "nipy_spectral",
    "Cubehelix": "cubehelix",
    "Oranges": "Oranges",
    "Plasma": "plasma",
    "Inferno": "inferno",
    "Pastel": "Pastel1",
    "Accent": "Accent",
    "Dark2": "Dark2",
    "Set1": "Set1",
    "Set2": "Set2",
    "Set3": "Set3",
    "tab10": "tab10",
    "tab20": "tab20",
    "tab20b": "tab20b",
    "tab20c": "tab20c",
    "twilight": "twilight",
    "twilight_shifted": "twilight_shifted",
    "hsv": "hsv",
    "flag": "flag",
    "prism": "prism",
    "ocean": "ocean",
    "gist_earth": "gist_earth",
    "terrain": "terrain",
    "gist_stern": "gist_stern",
    "gnuplot": "gnuplot",
    "gnuplot2": "gnuplot2",
    "CMRmap": "CMRmap",
    "cubehelix": "cubehelix",
    "brg": "brg",
    "gist_rainbow": "gist_rainbow",
    "rainbow": "rainbow",
    "jet": "jet",
    "turbo": "turbo",
    "nipy_spectral": "nipy_spectral",
    "gist_ncar": "gist_ncar",
}

# Streamlit UI
st.title("Scientific Paper Word Cloud Generator")

# Text area for pasting paragraphs
text = st.text_area("Paste your paragraphs here:")

# Checkbox to remove stop words
remove_stopwords = st.checkbox("Remove Stop Words")

# Generate word clouds for all color schemes
if st.button("Generate Word Clouds"):
    if text:
        for color_scheme_name, color_scheme in color_schemes.items():
            # Create a WordCloud object
            wordcloud = WordCloud(
                background_color="white",
                width=800,
                height=400,
                colormap=color_scheme,
                stopwords=STOPWORDS if remove_stopwords else None,
                max_words=100,  # You can adjust the number of words displayed
            )

            # Generate the word cloud
            wordcloud.generate(text)

            # Display the word cloud with the color scheme name
            st.subheader(f"Word Cloud ({color_scheme_name})")
            st.image(wordcloud.to_array(), use_column_width=True, channels="RGB")

    else:
        st.warning("Please enter some text to generate word clouds.")

# Information and tips
st.markdown("### Tips:")
st.write("- Paste your paragraphs into the text area.")
st.write("- You can choose to remove stop words to filter common words.")
st.write("- Click the 'Generate Word Clouds' button to display word clouds for all color schemes.")

# Footer
st.markdown("---")
st.write("Created by Your Name")
