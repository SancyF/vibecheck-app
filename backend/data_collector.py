# data_collector.py
import requests
import os
from textblob import TextBlob
# Remove problematic imports for Lambda
# import snscrape.modules.twitter as sntwitter
# import instaloader
class DataCollector:
    def __init__(self):
        try:
            self.weather_api = os.getenv('WEATHER_API_KEY')
            self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN')
            print(f"[INFO] DataCollector initialized - Weather API: {'✓' if self.weather_api else '✗'}")
        except Exception as e:
            print(f"[ERROR] DataCollector initialization failed: {e}")
            raise
    
    def get_weather_vibe(self, location):
        """Weather affects mood - sunny = positive vibes"""
        try:
            if not self.weather_api:
                print("[WARNING] No weather API key found, using default score")
                return {
                    'weather_score': 50,
                    'condition': 'unknown',
                    'temp': 0
                }
                
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api}"
            print(f"[DEBUG] Calling weather API: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                raise Exception(f"Weather API HTTP {response.status_code}: {response.text}")
                
            data = response.json()
            print(f"[DEBUG] Weather API response: {data}")
            
            if 'cod' in data and data['cod'] != 200:
                raise Exception(f"Weather API error: {data.get('message', 'Unknown error')}")
                
            if 'weather' not in data:
                raise Exception(f"Invalid weather API response structure: {data}")
                
            weather_score = 50  # baseline
            weather_main = data['weather'][0]['main']
            
            # Improve weather scoring
            if weather_main in ['Clear', 'Sunny']:
                weather_score = 75
            elif weather_main in ['Clouds', 'Partly Cloudy']:
                weather_score = 60
            elif weather_main in ['Rain', 'Drizzle']:
                weather_score = 35
            elif weather_main in ['Thunderstorm', 'Snow']:
                weather_score = 25
            else:
                weather_score = 50
                
            # Adjust for temperature (convert from Kelvin to Celsius)
            temp_celsius = data['main']['temp'] - 273.15
            if 20 <= temp_celsius <= 30:  # Comfortable temperature
                weather_score += 10
            elif temp_celsius > 35 or temp_celsius < 10:  # Extreme temperatures
                weather_score -= 10
                
            return {
                'weather_score': max(10, min(100, weather_score)),
                'condition': data['weather'][0]['description'],
                'temp': temp_celsius
            }
        except Exception as e:
            print(f"[ERROR] Weather API failed: {e}")
            return {
                'weather_score': 50,
                'condition': 'unknown',
                'temp': 0
            }
    
    def get_social_sentiment(self, location: str):
        """Analyze recent social posts (Twitter first, fallback to Instagram hashtags)"""

        posts = []
        source = "Unknown"


        # Always try Reddit for social data (Twitter is disabled)
        try:
            print(f"[INFO] Searching Reddit for: {location}")
            headers = {'User-agent': 'vibecheck-bot/1.0'}
            
            # Clean up location for better search
            search_term = location.replace(' ', '+')
            url = f"https://www.reddit.com/search.json?q={search_term}&limit=20&sort=relevance"
            print(f"[DEBUG] Reddit URL: {url}")
            
            response = requests.get(url, headers=headers, timeout=10)
            print(f"[DEBUG] Reddit response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG] Reddit data structure: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
                
                for post in data.get("data", {}).get("children", []):
                    post_data = post.get("data", {})
                    title = post_data.get("title", "")
                    selftext = post_data.get("selftext", "")[:100]  # First 100 chars
                    
                    if title:
                        posts.append(title)
                    if selftext and len(selftext) > 10:
                        posts.append(selftext)
                        
                if posts:
                    source = "Reddit"
                    print(f"[INFO] Found {len(posts)} Reddit posts for {location}")
                else:
                    print(f"[WARNING] No Reddit posts found for {location}")
            else:
                print(f"[ERROR] Reddit API returned status {response.status_code}")
                
        except Exception as e:
            print(f"[ERROR] Reddit fetch failed: {e}")
            import traceback
            print(traceback.format_exc())

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