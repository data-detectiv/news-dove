from bs4 import BeautifulSoup
from textblob import TextBlob
import requests

url='https://www.bbc.com/news'

response = requests.get(url).text
doc = BeautifulSoup(response, "html.parser")
headlines = doc.find_all("h2", {"data-testid": "card-headline"})

for headline in headlines:
    blob = TextBlob(headline.text)
    blob.tags
    blob.noun_phrases
    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)