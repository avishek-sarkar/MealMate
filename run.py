#!/usr/bin/env python3
"""
MealMate Flask Application Runner
"""

import os
from dotenv import load_dotenv
from app import app

# Load environment variables
load_dotenv()

if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🍔 Starting MealMate - Campus Food Hub")
    print(f"🌐 Running on http://{host}:{port}")
    print("🔄 Press Ctrl+C to stop the server")
    
    app.run(host=host, port=port, debug=debug)
