#!/usr/bin/env python3
"""
Simple test script for the Ukrainian Q&A API
"""

import requests
import json

def test_api():
    """Test the Ukrainian Q&A API"""
    
    print("🧪 Testing Ukrainian Q&A API...")
    print("=" * 40)
    
    # Test health endpoint
    try:
        response = requests.get('http://localhost:8000/api/health')
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test ask endpoint
    test_questions = [
        "What is the capital of Ukraine?",
        "Tell me about Ukrainian borscht",
        "What does Слава Україні mean?",
        "Hello"
    ]
    
    for question in test_questions:
        try:
            print(f"\n🤔 Testing: '{question}'")
            response = requests.post(
                'http://localhost:8000/api/ask',
                json={'question': question},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"   Success: {data.get('success')}")
                print(f"   Answer: {data.get('answer', 'No answer')[:100]}...")
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
