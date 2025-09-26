# 🎉 VibeCheck: Real-Time Event Atmosphere Predictor

VibeCheck is a smart Python-powered application that predicts the **real-time vibe** of a location or venue based on:

- 🌦️ **Weather data**
- 🗣️ **Social media sentiment** (Twitter, Reddit)
- 🎟️ **Local events** (coming soon)
- 🚶 **Crowd density** (planned)

Whether you're heading to a concert, planning a meetup, or avoiding crowded areas — VibeCheck gives you the **atmosphere score** of any place, anytime.

---

## 🚀 Features

- 🐦 Fetches real-time tweets using `snscrape`
- 👥 Fallback to Reddit posts when Twitter fails
- 💬 Sentiment analysis with `TextBlob`
- 🌤️ Weather info using OpenWeatherMap API
- 📊 Returns vibe score (0–100 scale)
- 📦 Easy to integrate into any app or dashboard
