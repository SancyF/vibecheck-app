import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Rate Limits
    MAX_TWEETS = 10
    CACHE_DURATION = 300  # 5 minutes
    
    # Default locations for demo
    DEMO_LOCATIONS = [
        "Marina Beach Chennai",
        "Phoenix MarketCity Chennai", 
        "T Nagar Chennai",
        "Anna Nagar Chennai",
        "Besant Nagar Chennai"
    ]