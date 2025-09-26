#!/bin/bash
echo "🚀 Setting up VibeCheck..."

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

echo "✅ Setup complete!"
echo "📝 Don't forget to:"
echo "   1. Copy .env.example to .env and add your API keys"
echo "   2. Run 'python backend/app.py' for backend"
echo "   3. Run 'npm start' in frontend/ for frontend"