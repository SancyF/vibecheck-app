# app.py - Complete version
from flask import Flask, jsonify
from flask_cors import CORS
import time
import traceback

app = Flask(__name__)
CORS(app)

# Initialize components with error handling
collector = None
analyzer = None

try:
    print("Attempting to import DataCollector...")
    from data_collector import DataCollector
    collector = DataCollector()
    print("✅ DataCollector imported and initialized")
except Exception as e:
    print(f"❌ DataCollector failed: {e}")
    traceback.print_exc()

try:
    print("Attempting to import VibeAnalyzer...")
    from ai_analyzer import VibeAnalyzer
    analyzer = VibeAnalyzer()
    print("✅ VibeAnalyzer imported and initialized")
except Exception as e:
    print(f"❌ VibeAnalyzer failed: {e}")
    traceback.print_exc()

if collector and analyzer:
    print("✅ All components initialized successfully")
else:
    print(f"⚠️  Warning: Some components failed - collector:{collector is not None}, analyzer:{analyzer is not None}")
@app.route("/")
def index():
    return jsonify({
        "message": "VibeCheck API is running!",
        "status": "healthy",
        "components": {
            "data_collector": collector is not None,
            "ai_analyzer": analyzer is not None
        }
    })

@app.route("/health")
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": int(time.time())
    })
@app.route('/api/vibe/<location>')
def get_vibe(location):
    try:
        # Collect data
        from urllib.parse import unquote
        decoded_location = unquote(location)
        print(f"🔍 Checking vibe for: {decoded_location} (original: {location})")
        
        # Initialize default data in case of failures
        weather_data = {'weather_score': 50, 'condition': 'unknown', 'temp': 20}
        social_data = {'posts': [], 'post_count': 0, 'sentiment_score': 50, 'source': 'None'}
        ai_analysis = {'ai_score': 50, 'vibe_description': 'Neutral Area'}
        
        # Try to get weather data
        if collector:
            try:
                weather_data = collector.get_weather_vibe(decoded_location)
                print(f"Weather Data: {weather_data}")
            except Exception as e:
                print(f"Weather collection failed: {e}")
        else:
            print("[WARNING] DataCollector not available")
        
        # Try to get social data
        if collector:
            try:
                social_data = collector.get_social_sentiment(decoded_location)
                print(f"Social Data: {social_data}")
            except Exception as e:
                print(f"Social collection failed: {e}")
        
        # AI analysis if we have social data and analyzer is available
        if analyzer and social_data['post_count'] > 0:
            try:
                print("Running AI analysis...")
                ai_analysis = analyzer.analyze_text_sentiment(social_data['posts'])
                print(f"AI Analysis: {ai_analysis}")
            except Exception as e:
                print(f"AI analysis failed: {e}")
        else:
            if not analyzer:
                print("[WARNING] VibeAnalyzer not available")
        
        # Calculate final vibe
        if analyzer:
            try:
                final_vibe = analyzer.calculate_final_vibe(weather_data, social_data, ai_analysis)
                print(f"Final Vibe: {final_vibe}")
            except Exception as e:
                print(f"Final vibe calculation failed: {e}")
                # Fallback vibe calculation
                final_vibe = {
                    'vibe_score': 50,
                    'category': '😐 Quiet Zone',
                    'description': 'Limited Data',
                    'factors': {
                        'weather': weather_data['weather_score'],
                        'social': ai_analysis['ai_score'],
                        'posts_analyzed': social_data['post_count']
                    }
                }
        else:
            # No analyzer available - basic calculation
            basic_score = (weather_data['weather_score'] + 50) // 2
            if basic_score >= 60:
                category = "✨ Good Vibes"
            elif basic_score >= 40:
                category = "😐 Quiet Zone"
            else:
                category = "💤 Low Energy"
                
            final_vibe = {
                'vibe_score': basic_score,
                'category': category,
                'description': 'Basic Analysis',
                'factors': {
                    'weather': weather_data['weather_score'],
                    'social': 50,
                    'posts_analyzed': social_data['post_count']
                }
            }
        
        return jsonify({
            'location': decoded_location,
            'timestamp': int(time.time()),
            'vibe': final_vibe,
            'raw_data': {
                'weather': weather_data,
                'social_mentions': social_data['post_count'],
                'sample_posts': social_data.get('posts', [])[:2]
            },
            'debug_info': {
                'components': {
                    'data_collector': collector is not None,
                    'ai_analyzer': analyzer is not None
                }
            }
        })
        
    except Exception as e:
        print(f"ERROR in get_vibe: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'error': f'Processing failed: {str(e)}',
            'location': decoded_location if 'decoded_location' in locals() else location,
            'timestamp': int(time.time())
        }), 500

@app.route('/api/locations')
def popular_locations():
    # Updated demo locations that should work well
    demo_locations = [
        "Chennai",
        "Kochi", 
        "Mumbai",
        "Delhi",
        "Bangalore",
        "Marina Beach",
        "Goa",
        "Mysore"
    ]
    return jsonify({'locations': demo_locations})
@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print(traceback.format_exc())
    return jsonify(error=str(e)), 500
if __name__ == '__main__':
    app.run(debug=True)