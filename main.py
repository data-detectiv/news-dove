from bs4 import BeautifulSoup
from textblob import TextBlob
from datetime import datetime, timedelta
import requests
import pandas as pd
import re

url='https://www.bbc.com/news'

response = requests.get(url).text
doc = BeautifulSoup(response, "html.parser")
headlines = doc.find_all("h2", {"data-testid": "card-headline"})
timestamps = doc.find_all("span", {"data-testid":"card-metadata-lastupdated"})


start_time = datetime.now()
def convert_to_hours(time_str):
    """
    This function convert one unit to the other to ensure 
    consistency with the unit of measuring time
    """
    if 'hrs' in time_str:
        hours = int(re.search(r'\d+', time_str).group())
        return hours
    elif 'mins' in time_str:
        mins = int(re.search(r'\d+', time_str).group())
        return round(mins/60, 2)
    else:
        return 0

data = []
for headline in headlines:
    blob = TextBlob(headline.text)
    blob.tags
    blob.noun_phrases

    for timestamp in timestamps:
        timestamp_in_hours = convert_to_hours(timestamp.text)
        headline_time = (start_time + timedelta(hours=timestamp_in_hours)).strftime('%Y-%m-%d %H:%M:%S')
        
       
        for sentence in blob.sentences:
            sentiment_score = sentence.sentiment.polarity
            if sentiment_score > 0:
                sentiment_label = "Positive"
            elif sentiment_score < 0:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
            
            data.append({
                "headline": headline.text, 
                "sentiment_score": sentiment_score,
                "sentiment_label": sentiment_label,
                "timestamp": headline_time})

df = pd.DataFrame(data).sort_values(by='timestamp').reset_index(drop=True)
df = df.drop_duplicates()
df.to_csv('news_sentiment.csv', index=False)



