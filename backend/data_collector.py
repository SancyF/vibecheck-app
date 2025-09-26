# data_collector.py
import requests
import os
import snscrape.modules.twitter as sntwitter
import instaloader
USERNAME = "sancyfrancis"
SESSION_FILE = r"C:\Users\Sancy Francis\AppData\Local\Instaloader\session-sancyfrancis"
class DataCollector:
    def __init__(self):
        self.weather_api = os.getenv('WEATHER_API_KEY')
        self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN')
    
    def get_weather_vibe(self, location):
        """Weather affects mood - sunny = positive vibes"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api}"
        response = requests.get(url).json()
        print(f"[DEBUG] Weather API response: {response}")
        weather_score = 50  # baseline
        if 'Clear' in response['weather'][0]['main']:
            weather_score += 20
        elif 'Rain' in response['weather'][0]['main']:
            weather_score -= 15
            
        return {
            'weather_score': weather_score,
            'condition': response['weather'][0]['description'],
            'temp': response['main']['temp']
        }
    
    def get_social_sentiment(self, location: str):
        """Analyze recent social posts (Twitter first, fallback to Instagram hashtags)"""

        posts = []
        source = "Unknown"


        # Fallback to Reddit if Twitter fails or returns no posts
        if not posts:
            try:
                print(f"[INFO] Falling back to Reddit for: {location}")
                headers = {'User-agent': 'vibecheck-bot'}
                url = f"https://www.reddit.com/search.json?q={location}&limit=20"
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    for post in data.get("data", {}).get("children", []):
                        title = post["data"].get("title", "")
                        if title:
                            posts.append(title)
                if posts:
                    source = "Reddit"
            except Exception as e:
                print(f"[ERROR] Reddit fetch failed: {e}")

        # Sentiment Analysis
        try:
            sentiments = [TextBlob(p).sentiment.polarity for p in posts if p]
            sentiment_score = (sum(sentiments) / len(sentiments)) * 50 + 50 if sentiments else 50
        except Exception as e:
            print(f"[ERROR] Sentiment analysis failed: {e}")
            sentiment_score = 50

        return {
            "posts": posts[:5],  # Top 5 posts only
            "post_count": len(posts),
            "sentiment_score": round(sentiment_score, 2),
            "source": source
        }