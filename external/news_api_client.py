from newsapi import NewsApiClient
import json
from dotenv import load_dotenv
import os

load_dotenv()

# Init
print(os.getenv("NEWS_API_KEY"))
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))

result = newsapi.get_top_headlines(country='us')
print(result["status"])

print(json.dumps(result["articles"]))
