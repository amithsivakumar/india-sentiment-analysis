import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import requests
from datetime import datetime

# --- CONFIGURATION ---
# Get your free key at newsapi.org
API_KEY = "6ee040b6e37d4f3ab1296ef004af035e" 

class NewsEngine:
    """Handles real-time data fetching from NewsAPI."""
    
    def fetch_real_time(self, topic):
        # We query news articles to simulate social media 'posts'
        url = f'https://newsapi.org/v2/everything?q={topic}&language=en&sortBy=publishedAt&apiKey={API_KEY}'
        
        try:
            response = requests.get(url)
            data = response.json()
            articles = data.get('articles', [])
            
            # Formatting the data for our analysis
            clean_posts = []
            for art in articles[:15]: # Take top 15 latest results
                clean_posts.append({
                    "text": art['title'], # Using headlines as our 'posts'
                    "date": art['publishedAt'][:10],
                    "source": art['source']['name']
                })
            return clean_posts
        except:
            # Fallback if API fails or Key is missing
            return [{"text": "Error connecting to live API. Check your API Key.", "date": str(datetime.now().date()), "source": "System"}]

def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0: return "Positive", score
    elif score < 0: return "Negative", score
    else: return "Neutral", score

# --- STREAMLIT UI ---
st.set_page_config(page_title="India Real-Time Analyzer", layout="wide")

st.title("🇮🇳 Real-Time Trend & Sentiment Analyzer")
st.sidebar.info("This app pulls LIVE headlines using NewsAPI to analyze current sentiment.")

topic_map = {
    "Elections": "India Elections 2026",
    "IPL": "IPL Cricket CSK RCB MI",
    "Movies": "Bollywood Movies 2026"
}

topic_choice = st.sidebar.selectbox("Choose Live Topic", list(topic_map.keys()))
run_btn = st.sidebar.button("Fetch Live Data")

if run_btn:
    engine = NewsEngine()
    with st.spinner('Fetching live data from the cloud...'):
        posts = engine.fetch_real_time(topic_map[topic_choice])
        
        if posts:
            df = pd.DataFrame(posts)
            # Add Sentiment
            df[['Sentiment', 'Score']] = df['text'].apply(lambda x: pd.Series(get_sentiment(x)))
            
            # --- DASHBOARD ---
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader("Sentiment Summary")
                sentiment_counts = df['Sentiment'].value_counts()
                fig, ax = plt.subplots()
                sentiment_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#66b3ff','#99ff99','#ff9999'], ax=ax)
                st.pyplot(fig)
                
            with col2:
                st.subheader("Live Mentions")
                st.dataframe(df[['text', 'Sentiment']], use_container_width=True)

            st.divider()
            st.subheader("Daily Sentiment Polarity")
            st.line_chart(df.set_index('date')['Score'])
            
            # Save for report
            df.to_csv("latest_report.csv")
            st.success("Analysis Complete. Report saved as CSV.")
        else:
            st.error("Could not find any live data for this topic right now.")
else:
    st.warning("👈 Enter your API Key in the code and click 'Fetch Live Data' to see it in action!")
