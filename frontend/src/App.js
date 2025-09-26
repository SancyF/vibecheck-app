import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [location, setLocation] = useState('');
  const [vibeData, setVibeData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [popularLocations, setPopularLocations] = useState([]);

  useEffect(() => {
    // Load popular locations
    fetch('http://localhost:5000/api/locations')
      .then(res => res.json())
      .then(data => {
        console.log('Locations data:', data);
        setPopularLocations(data.locations || []);
      })
      .catch(err => {
        console.error('Error loading locations:', err);
        setPopularLocations([]);
      });
  }, []);

  const checkVibe = async () => {
    if (!location) return;
    
    setLoading(true);
    setVibeData(null); // Clear previous data
    
    try {
      const cleanLocation = location.trim();
      const encodedLocation = encodeURIComponent(cleanLocation);
      
      console.log('Checking vibe for:', cleanLocation);
      console.log('Encoded URL:', encodedLocation);
      const response = await fetch(`http://localhost:5000/api/vibe/${encodeURIComponent(encodedLocation)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      
      // Check if response has error
      if (data.error) {
        setVibeData({ error: data.error });
        return;
      }
      
      // Validate required data structure
      if (!data.vibe || typeof data.vibe.vibe_score === 'undefined') {
        console.error('Invalid API response structure:', data);
        setVibeData({ 
          error: 'Invalid response from server. Please try again.',
          debug: data 
        });
        return;
      }
      
      setVibeData(data);
    } catch (error) {
      console.error('Error fetching vibe data:', error);
      setVibeData({ 
        error: `Failed to check vibe: ${error.message}` 
      });
    } finally {
      setLoading(false);
    }
  };

  const getVibeColor = (score) => {
    if (!score) return '#96ceb4';
    if (score >= 75) return '#ff6b6b';
    if (score >= 60) return '#4ecdc4';
    if (score >= 40) return '#45b7d1';
    return '#96ceb4';
  };

  const getVibeEmoji = (score) => {
    if (!score) return '💤';
    if (score >= 75) return '🔥';
    if (score >= 60) return '✨';
    if (score >= 40) return '😐';
    return '💤';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-600 via-pink-600 to-blue-600 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            VibeCheck 🌟
          </h1>
          <p className="text-xl text-white opacity-90">
            Discover the real-time atmosphere of any location using AI-powered sentiment analysis
          </p>
        </div>

        {/* Search Section */}
        <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8 mb-8">
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <input
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="Enter location (e.g., Marina Beach Chennai)"
              className="flex-1 px-6 py-4 rounded-2xl bg-white/20 text-white placeholder-white/70 border border-white/30 focus:outline-none focus:ring-2 focus:ring-white/50"
              onKeyPress={(e) => e.key === 'Enter' && checkVibe()}
            />
            <button
              onClick={checkVibe}
              disabled={loading}
              className="px-8 py-4 bg-white text-purple-600 font-bold rounded-2xl hover:bg-white/90 transition-all disabled:opacity-50"
            >
              {loading ? 'Checking Vibe...' : 'Check Vibe ✨'}
            </button>
          </div>

          {/* Popular Locations */}
          <div className="flex flex-wrap gap-2">
            <span className="text-white/70 text-sm">Popular: </span>
            {popularLocations.map((loc, idx) => (
              <button
                key={idx}
                onClick={() => setLocation(loc)}
                className="px-3 py-1 bg-white/20 text-white text-sm rounded-full hover:bg-white/30 transition-all"
              >
                {loc}
              </button>
            ))}
          </div>
        </div>

        {/* Results Section */}
        {vibeData && vibeData.vibe && (
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-8">
            <div className="text-center mb-8">
              <h2 className="text-3xl font-bold text-white mb-2">
                {vibeData.location || 'Unknown Location'}
              </h2>
              <p className="text-white/70">
                Last updated: {vibeData.timestamp ? new Date(vibeData.timestamp * 1000).toLocaleTimeString() : 'Just now'}
              </p>
            </div>

            {/* Main Vibe Display */}
            <div className="text-center mb-8">
              <div 
                className="inline-block w-32 h-32 rounded-full flex items-center justify-center text-4xl font-bold text-white mb-4"
                style={{ backgroundColor: getVibeColor(vibeData.vibe?.vibe_score) }}
              >
                {vibeData.vibe?.vibe_score || '??'}
              </div>
              <h3 className="text-2xl font-bold text-white mb-2">
                {getVibeEmoji(vibeData.vibe?.vibe_score)} {vibeData.vibe?.category || 'Unknown Vibe'}
              </h3>
              <p className="text-xl text-white/80">
                {vibeData.vibe?.description || 'No description available'}
              </p>
            </div>

            {/* Factors Breakdown */}
            {vibeData.vibe?.factors && (
              <div className="grid md:grid-cols-3 gap-6 mb-8">
                <div className="text-center">
                  <div className="text-2xl mb-2">🌤️</div>
                  <div className="text-white font-semibold">Weather</div>
                  <div className="text-white/70">{vibeData.vibe.factors.weather || 'N/A'}/100</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-2">🗣️</div>
                  <div className="text-white font-semibold">Social Buzz</div>
                  <div className="text-white/70">{vibeData.vibe.factors.social || 'N/A'}/100</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl mb-2">📊</div>
                  <div className="text-white font-semibold">Data Points</div>
                  <div className="text-white/70">{vibeData.vibe.factors.posts_analyzed || 0} posts</div>
                </div>
              </div>
            )}

            {/* Sample Posts */}
            {vibeData.raw_data?.sample_posts && vibeData.raw_data.sample_posts.length > 0 && (
              <div>
                <h4 className="text-lg font-semibold text-white mb-4">Recent Mentions:</h4>
                <div className="space-y-3">
                  {vibeData.raw_data.sample_posts.map((post, idx) => (
                    <div key={idx} className="bg-white/10 p-4 rounded-xl">
                      <p className="text-white/90 text-sm">"{post.substring(0, 150)}..."</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Loading State */}
        {loading && (
          <div className="text-center">
            <div className="animate-pulse text-white text-xl">
              Analyzing vibes... 🔮
            </div>
          </div>
        )}

        {/* Error State */}
        {vibeData && vibeData.error && (
          <div className="bg-red-500/20 backdrop-blur-lg rounded-3xl p-8 text-center">
            <h3 className="text-xl font-bold text-white mb-2">Oops! Something went wrong</h3>
            <p className="text-white/80">{vibeData.error}</p>
            <button 
              onClick={() => setVibeData(null)}
              className="mt-4 px-6 py-2 bg-white/20 text-white rounded-xl hover:bg-white/30"
            >
              Try Again
            </button>
          </div>
        )}

        {/* Demo Notice */}
        <div className="text-center mt-8">
          <p className="text-white/60 text-sm">
            VibeCheck uses real-time social media sentiment, weather data, and AI analysis
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;