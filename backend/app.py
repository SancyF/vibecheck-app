# app.py - Complete version
#import ssl_fix
from flask import Flask, jsonify
from flask_cors import CORS
from data_collector import DataCollector
from ai_analyzer import VibeAnalyzer
import time

app = Flask(__name__)
CORS(app)

collector = DataCollector()
analyzer = VibeAnalyzer()

@app.route('/api/vibe/<location>')
def get_vibe(location):
    try:
        # Collect data
        from urllib.parse import unquote
        decoded_location = unquote(location)
        print(f"🔍 Checking vibe for: {decoded_location} (original: {location})")
        
        weather_data = collector.get_weather_vibe(decoded_location)
        print(f"Weather Data: {weather_data}")
        social_data = collector.get_social_sentiment(location)
        print(f"Social Data: {social_data}")
        # AI analysis if we have social data
        if social_data['post_count'] > 0:
            print("Running AI analysis...")
            ai_analysis = analyzer.analyze_text_sentiment(social_data['posts'])
        else:
            ai_analysis = {'ai_score': 45, 'vibe_description': 'Quiet Area'}
        print(f"AI Analysis: {ai_analysis}")
        # Calculate final vibe
        final_vibe = analyzer.calculate_final_vibe(weather_data, social_data, ai_analysis)
        print(f"Final Vibe: {final_vibe}")
        return jsonify({
            'location': location,
            'timestamp': int(time.time()),
            'vibe': final_vibe,
            'raw_data': {
                'weather': weather_data,
                'social_mentions': social_data['post_count'],
                'sample_posts': social_data.get('posts', [])[:2]
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/locations')
def popular_locations():
    # Demo data for quick testing
    demo_locations = [
        "Ernakulam"
    ]
    return jsonify({'locations': demo_locations})

if __name__ == '__main__':
    app.run(debug=True)