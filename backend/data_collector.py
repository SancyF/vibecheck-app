# data_collector.py
import requests
import os
import snscrape.modules.twitter as sntwitter
import instaloader

class DataCollector:
    def __init__(self):
        self.weather_api = os.getenv('WEATHER_API_KEY')
        self.twitter_bearer = os.getenv('TWITTER_BEARER_TOKEN')
    
    def get_weather_vibe(self, location):
        """Weather affects mood - sunny = positive vibes"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api}"
        response = requests.get(url).json()
        
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

        tweets = []
        try:
            # Try Twitter first
            query = f"{location} lang:en"
            for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
                if i >= 20:
                    break
                tweets.append(tweet.content)
        except Exception as e:
            print(f"Twitter fetch failed: {e}")

        # If Twitter failed or returned no results → fallback to Instagram
        if not tweets:
            try:
                import ssl
                ssl._create_default_https_context = ssl._create_unverified_context
                print(f"Falling back to Instagram hashtag search for: {location}")
                L = instaloader.Instaloader(download_pictures=False,
                                            download_videos=False,
                                            download_comments=False,
                                            save_metadata=False,
                                            download_video_thumbnails=False,
                                            quiet=True)
                posts = instaloader.Hashtag.from_name(L.context, location.lower()).get_posts()

                for i, post in enumerate(posts):
                    if i >= 20:
                        break
                    tweets.append(post.caption or "")
            except Exception as e:
                print(f"Instagram fetch failed: {e}")

        # Sentiment analysis (basic, optional)
        try:
            from textblob import TextBlob
            sentiments = [TextBlob(t).sentiment.polarity for t in tweets if t]
            sentiment_score = (sum(sentiments) / len(sentiments) * 50) + 50 if sentiments else 50
        except ImportError:
            sentiment_score = 50

        return {
            "posts": tweets[:5],      # Top 5 posts (tweets or Instagram captions)
            "post_count": len(tweets),
            "sentiment_score": round(sentiment_score, 2),
            "source": "Twitter" if tweets and "Twitter" in str(type(tweets[0])) else "Instagram"
        }