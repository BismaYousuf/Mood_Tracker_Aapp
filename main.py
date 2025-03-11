import streamlit as st
import pandas as pd
import datetime
import csv
import os
import plotly.express as px  # For better charts

# Define the file name for storing mood data
MOOD_FILE = "mood_log.csv"

# Function to read mood data from the CSV file
def load_mood_data():
    if not os.path.exists(MOOD_FILE):
        return pd.DataFrame(columns=["Date", "Mood"])
    return pd.read_csv(MOOD_FILE)

# Function to add new mood entry to CSV file
def save_mood_data(date, mood):
    with open(MOOD_FILE, "a") as file:
        writer = csv.writer(file)
        writer.writerow([date, mood])

# Streamlit app UI
st.set_page_config(page_title="Mood Tracker", page_icon="😊", layout="wide")
st.title("📅 Mood Tracker")

# Sidebar for user input
st.sidebar.header("Log Your Mood")
today = datetime.date.today()

# Emoji-based mood selection
moods = {"😀 Happy": "Happy", "😢 Sad": "Sad", "😡 Angry": "Angry", "😐 Neutral": "Neutral"}
selected_mood = st.sidebar.selectbox("How are you feeling today?", list(moods.keys()))

if st.sidebar.button("Log Mood", use_container_width=True):
    save_mood_data(today, moods[selected_mood])
    st.sidebar.success("✅ Mood Logged Successfully!")

# Load existing mood data
data = load_mood_data()
if not data.empty:
    st.subheader("📊 Mood Trends Over Time")
    data["Date"] = pd.to_datetime(data["Date"])
    mood_counts = data.groupby("Mood").count()["Date"].reset_index()
    
    # Use Plotly for a better bar chart
    fig = px.bar(mood_counts, x="Mood", y="Date", color="Mood",
                 labels={"Date": "Mood Count"}, title="Mood Frequency")
    st.plotly_chart(fig, use_container_width=True)
    
    # Display recent moods
    st.subheader("📌 Recent Mood Logs")
    st.dataframe(data.tail(5))

# Footer
st.markdown("---")
st.markdown("### Built with ❤️ by Bisma Yousuf")