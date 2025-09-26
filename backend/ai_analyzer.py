# ai_analyzer.py
import openai
import os

class VibeAnalyzer:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def analyze_text_sentiment(self, texts):
        """Use OpenAI to analyze sentiment of social media posts"""
        combined_text = " ".join(texts[:3])  # Limit for API costs
        
        prompt = f"""
        Analyze the overall vibe/sentiment of these social media posts about a location.
        Rate from 0-100 where:
        - 0-30: Very negative/dangerous vibes
        - 30-50: Neutral/quiet vibes  
        - 50-70: Good/positive vibes
        - 70-100: Amazing/exciting vibes
        
        Posts: {combined_text}
        
        Respond with just a number and 2-word description (e.g., "75 Energetic Fun"):
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20
            )
            
            result = response.choices[0].message.content.strip()
            score = int(result.split()[0])
            description = " ".join(result.split()[1:3])
            
            return {'ai_score': score, 'vibe_description': description}
            
        except:
            return {'ai_score': 50, 'vibe_description': 'Neutral Quiet'}
    
    def calculate_final_vibe(self, weather_data, social_data, ai_analysis):
        """Combine all factors into final vibe score"""
        base_score = 40
        
        # Weight different factors
        weather_weight = 0.3
        social_weight = 0.4  
        ai_weight = 0.3
        
        final_score = (
            weather_data['weather_score'] * weather_weight +
            ai_analysis['ai_score'] * ai_weight +
            base_score * 0.3  # baseline
        )
        
        # Determine vibe category
        if final_score >= 75:
            category = "🔥 Hot Spot"
        elif final_score >= 60:
            category = "✨ Good Vibes" 
        elif final_score >= 40:
            category = "😐 Quiet Zone"
        else:
            category = "💤 Low Energy"
            
        return {
            'vibe_score': min(100, max(0, int(final_score))),
            'category': category,
            'description': ai_analysis['vibe_description'],
            'factors': {
                'weather': weather_data['weather_score'],
                'social': ai_analysis['ai_score'],
                'tweets_analyzed': social_data['tweet_count']
            }
        }