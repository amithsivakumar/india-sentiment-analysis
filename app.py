import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import re

# --- 1. DATA LAYER (Simulating an API with more data) ---
class DataProvider:
    def __init__(self):
        self.mock_data = {
            "India Elections 2026": [
                {"text": "Excited for #IndiaElections2026! Hope for progress.", "date": "2026-05-03"},
                {"text": "Economic policies need a major overhaul. #India", "date": "2026-05-03"},
                {"text": "Digital India is reaching new heights. #Growth", "date": "2026-05-04"},
                {"text": "The new manifestos look promising for the youth.", "date": "2026-05-04"},
                {"text": "High inflation is a concern for voters. #Economy", "date": "2026-05-05"},
                {"text": "Proud of our democratic process. #VoterPride", "date": "2026-05-05"},
                {"text": "Infrastructure development is visible everywhere.", "date": "2026-05-05"}
            ],
            "IPL 2026 – CSK vs MI": [
                {"text": "Dhoni's last-ball six! Unbelievable! #CSK #IPL2026", "date": "2026-05-03"},
                {"text": "Bumrah's yorkers are still unplayable. #MI", "date": "2026-05-03"},
                {"text": "Worst pitch conditions for a T20 match.", "date": "2026-05-05"},
                {"text": "The atmosphere at Chepauk is electric! #WhistlePodu", "date": "2026-05-05"}
            ],
            "Movie: Bahubali 3": [
                {"text": "Bahubali 3 trailer is out! Pure goosebumps. #Prabhas", "date": "2026-05-03"},
                {"text": "The VFX quality is Hollywood level. #Bahubali3", "date": "2026-05-03"},
                {"text": "The storyline feels a bit recycled. #Disappointed", "date": "2026-05-05"}
            ]
        }
    def fetch_posts(self, topic):
        return self.mock_data.get(topic, [])

# --- 2. LOGIC LAYER ---
def analyze_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0: return "Positive", score
    elif score < 0: return "Negative", score
    else: return "Neutral", score

# --- 3. UI LAYER ---
st.set_page_config(page_title="India Trend Analyzer", layout="wide")
st.title("📊 Social Media Trend & Sentiment Analyzer")
st.sidebar.header("Options")
topic_choice = st.sidebar.selectbox("Select Topic", list(DataProvider().mock_data.keys()))

if st.sidebar.button("Analyze"):
    data = DataProvider().fetch_posts(topic_choice)
    df = pd.DataFrame(data)
    df[['Sentiment', 'Score']] = df['text'].apply(lambda x: pd.Series(analyze_sentiment(x)))

    # Metrics
    c1, c2 = st.columns(2)
    c1.metric("Total Posts", len(df))
    c2.metric("Avg Sentiment", round(df['Score'].mean(), 2))

    # Charts
    fig, ax = plt.subplots()
    df['Sentiment'].value_counts().plot(kind='bar', color=['green', 'red', 'gray'], ax=ax)
    st.pyplot(fig)
    
    st.table(df[['text', 'Sentiment']])
