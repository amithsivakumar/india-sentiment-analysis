import streamlit as st
import pandas as pd
from textblob import TextBlob
import requests

# 1. SETUP: Your API Key from NewsAPI.org
API_KEY = "6ee040b6e37d4f3ab1296ef004af035e"

# 2. APP TITLE
st.title("🇮🇳 Simple Social Media Analyzer")
st.write("First Year Mini-Project: MBCET")

# 3. SIDEBAR: User Input
topic = st.sidebar.selectbox("Select a Topic", ["Elections", "IPL Cricket", "Movies"])
btn = st.sidebar.button("Fetch Live Data")

if btn:
    # 4. FETCH: Getting real data from the web
    url = f'https://newsapi.org/v2/everything?q={topic}&apiKey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    articles = data.get('articles', [])

    # 5. PROCESS: Storing headlines in a list
    headlines = []
    for art in articles[:10]: # Just take 10 headlines to keep it simple
        headlines.append(art['title'])

    # 6. ANALYSIS: Checking Sentiment
    results = []
    for h in headlines:
        # Get polarity: -1 (Negative) to +1 (Positive)
        score = TextBlob(h).sentiment.polarity
        
        if score > 0:
            mood = "Positive"
        elif score < 0:
            mood = "Negative"
        else:
            mood = "Neutral"
        
        results.append({"Headline": h, "Sentiment": mood})

    # 7. DISPLAY: Show the table and a simple bar chart
    df = pd.DataFrame(results)
    
    st.subheader(f"Current Mood for: {topic}")
    st.table(df) # Simple table

    st.subheader("Sentiment Count")
    st.bar_chart(df['Sentiment'].value_counts()) # Built-in Streamlit chart

    # 8. SAVE: Automatic File Handling
    df.to_csv("my_project_data.csv", index=False)
    st.success("Results saved to CSV!")
