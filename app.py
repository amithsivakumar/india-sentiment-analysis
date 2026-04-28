import nltk
nltk.download('punkt_tab')
import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

# 1. Page Setup
st.title("🇮🇳 India Social Media Analyzer")
st.markdown("Analyzing trends in **Elections, Movies, and Cricket**")

# 2. Sidebar for User Choice
topic = st.sidebar.selectbox("Choose a Topic", ["Elections", "IPL Cricket", "Bollywood"])

# 3. Simple Data (In a real project, this comes from an API)
data = {
    "Elections": ["Voters are excited for the rally", "New policies are confusing", "Great turnout at the polls"],
    "IPL Cricket": ["Kohli played an amazing innings!", "The match was quite boring today", "Unbelievable catch by the fielder!"],
    "Bollywood": ["The new movie is a total flop", "Incredible acting by the lead", "The music is trending everywhere"]
}

# 4. Sentiment Logic
posts = data[topic]
results = []

for p in posts:
    score = TextBlob(p).sentiment.polarity
    if score > 0:
        sentiment = "Positive"
    elif score < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    results.append({"Post": p, "Sentiment": sentiment})

# 5. Show Results
df = pd.DataFrame(results)
st.table(df)

# 6. Chart
fig, ax = plt.subplots()
df['Sentiment'].value_counts().plot(kind='bar', ax=ax, color=['green', 'red', 'gray'])
st.pyplot(fig)