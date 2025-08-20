#!/usr/bin/env python3
"""
Startup script for the Ukrainian Q&A application
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'openai', 'sentence_transformers', 'faiss', 'numpy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def setup_environment():
    """Set up environment variables"""
    # Create .env file if it doesn't exist
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        try:
            with open('config.env.example', 'r') as f:
                template = f.read()
            with open('.env', 'w') as f:
                f.write(template)
            print("✅ Created .env file")
        except FileNotFoundError:
            print("⚠️  config.env.example not found, skipping .env creation")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
    except ImportError:
        print("⚠️  python-dotenv not installed, using system environment")

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting Ukrainian Q&A Application...")
    print("=" * 50)
    
    try:
        # Import and run the app
        from app import app
        
        print("✅ Application imported successfully")
        print("🌐 Starting web server...")
        print("📱 Open your browser and go to: http://localhost:5000")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        # Run the app
        app.run(host='0.0.0.0', port=5000, debug=False)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("Check the logs above for more details")

def main():
    """Main startup function"""
    print("🇺🇦 Ukrainian Q&A Application Startup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Start application
    start_application()

if __name__ == "__main__":
    main()
