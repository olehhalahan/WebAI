#!/usr/bin/env python3
"""
Simple test script for the Ukrainian Q&A application
"""

import requests
import time
import json

def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get('http://localhost:5000/api/health')
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return data.get('model_loaded', False)
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure the app is running.")
        return False

def test_question_endpoint(question):
    """Test the question endpoint with a sample question"""
    print(f"🤔 Testing question: '{question}'")
    try:
        response = requests.post(
            'http://localhost:5000/api/ask',
            json={'question': question},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Answer: {data['answer']}")
                return True
            else:
                print(f"❌ Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Request failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server.")
        return False

def main():
    """Run all tests"""
    print("🇺🇦 Ukrainian Q&A Application Test Suite")
    print("=" * 50)
    
    # Test health endpoint
    model_ready = test_health_endpoint()
    
    if not model_ready:
        print("⚠️  Model not ready, waiting 10 seconds...")
        time.sleep(10)
        model_ready = test_health_endpoint()
    
    if not model_ready:
        print("❌ Model still not ready. Please check the application logs.")
        return
    
    print("\n🧪 Testing sample questions...")
    
    # Test questions
    test_questions = [
        "What is the capital of Ukraine?",
        "Tell me about Ukrainian borscht",
        "What does Слава Україні mean?",
        "Ukrainian independence history"
    ]
    
    success_count = 0
    for question in test_questions:
        print(f"\n--- Testing: {question} ---")
        if test_question_endpoint(question):
            success_count += 1
        time.sleep(1)  # Small delay between requests
    
    print(f"\n📊 Test Results: {success_count}/{len(test_questions)} questions answered successfully")
    
    if success_count == len(test_questions):
        print("🎉 All tests passed! The application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the application logs for details.")

if __name__ == "__main__":
    main()
