"""
Test file for main.py FastAPI application
Run with: python test_main.py
"""

import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the API
BASE_URL = "http://localhost:25050"  # Change port if different

def test_health_check():
    """Test the /health endpoint"""
    print("\n" + "="*60)
    print("🧪 Testing /health endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print("❌ Health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running!")
        print(f"   Run: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_simulate_endpoint():
    """Test the /simulate endpoint"""
    print("\n" + "="*60)
    print("🧪 Testing /simulate endpoint")
    print("="*60)
    
    # Test data
    test_data = {
        "bot_id": 177,
        "user_prompt": """
TITLE: Role-Play: Cuong's Interactive Learning Adventure

ROLE: You are Cuong (6 years old, Vietnam).
Age & Level: 6 years old, English level A1.
Personality: Intelligent, enjoys experimenting.
Hobbies: Puzzle games, solving puzzles, reading comics.
Communication style: Logical curiosity, but childlike.
Learning goals: Learn English through intellectual activities.

TASK:
- Follow each step the ROBOT guides you.

RESPONSE TEMPLATE:
- Respond in Vietnamese.
- Super short answers with phrases.
- Answer 2–3 phrases max, EACH PHRASE 3–4 WORDS.
- WRITE ON ONE LINE ONLY, PHRASES SEPARATED BY PERIODS. NO LINE BREAKS.
- Use "Tớ" (self) and "Cậu" (the other).
- NO icons. NO emoji.
        """,
        "max_turns": 2,  # Small number for quick test
        "history": [{"role": "roleA", "content": "sẵn sàng"}]
    }
    
    try:
        print(f"Sending request to {BASE_URL}/simulate")
        print(f"Bot ID: {test_data['bot_id']}")
        print(f"Max turns: {test_data['max_turns']}")
        
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/simulate",
            json=test_data,
            timeout=300  # 5 minutes timeout for simulation
        )
        elapsed_time = time.time() - start_time
        
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Time: {elapsed_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Simulation completed successfully")
            print(f"Success: {result.get('success', False)}")
            print(f"Conversation length: {len(result.get('conversation', []))} messages")
            
            if result.get('conversation'):
                print("\n📝 First few messages:")
                for i, msg in enumerate(result['conversation'][:4]):
                    print(f"  {i+1}. [{msg.get('role', 'unknown')}]: {msg.get('content', '')[:100]}")
            
            if result.get('error'):
                print(f"\n⚠️  Error in result: {result['error']}")
            
            return True
        else:
            print(f"❌ Simulation failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (simulation took too long)")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running!")
        print(f"   Run: python main.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return False


def test_check_dod_endpoint():
    """Test the /check-dod-gen-feedback endpoint"""
    print("\n" + "="*60)
    print("🧪 Testing /check-dod-gen-feedback endpoint")
    print("="*60)
    
    test_data = {
        "inputs": {
            "conversation": "Test conversation",
            "DoD": "Test DoD"
        },
        "response_mode": "blocking",
        "user": "test_user"
    }
    
    try:
        print(f"Sending request to {BASE_URL}/check-dod-gen-feedback")
        
        response = requests.post(
            f"{BASE_URL}/check-dod-gen-feedback",
            json=test_data,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Check DoD endpoint responded")
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)[:500]}")
            return True
        else:
            print(f"❌ Check DoD failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_generate_report_endpoint():
    """Test the /generate-report endpoint"""
    print("\n" + "="*60)
    print("🧪 Testing /generate-report endpoint")
    print("="*60)
    
    test_data = {
        "conversation": "This is a test conversation for report generation."
    }
    
    try:
        print(f"Sending request to {BASE_URL}/generate-report")
        
        response = requests.post(
            f"{BASE_URL}/generate-report",
            json=test_data,
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Generate report endpoint responded")
            print(f"Response keys: {list(result.keys())}")
            return True
        else:
            print(f"❌ Generate report failed with status {response.status_code}")
            print(f"Response: {response.text[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("🚀 STARTING TESTS FOR SIMULATION API")
    print("="*60)
    print(f"Base URL: {BASE_URL}")
    print(f"Make sure the server is running: python main.py")
    print("="*60)
    
    # Check if OPENAI_API_KEY is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️  WARNING: OPENAI_API_KEY not found in environment")
        print("   Some tests may fail without it")
    
    results = []
    
    # Test 1: Health check
    results.append(("Health Check", test_health_check()))
    
    # Test 2: Simulate endpoint (only if health check passes)
    if results[0][1]:
        results.append(("Simulate Endpoint", test_simulate_endpoint()))
    else:
        print("\n⏭️  Skipping simulate test (server not available)")
        results.append(("Simulate Endpoint", False))
    
    # Test 3: Check DoD endpoint
    if results[0][1]:
        results.append(("Check DoD Endpoint", test_check_dod_endpoint()))
    else:
        print("\n⏭️  Skipping check-dod test (server not available)")
        results.append(("Check DoD Endpoint", False))
    
    # Test 4: Generate Report endpoint
    if results[0][1]:
        results.append(("Generate Report Endpoint", test_generate_report_endpoint()))
    else:
        print("\n⏭️  Skipping generate-report test (server not available)")
        results.append(("Generate Report Endpoint", False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("="*60)
    print(f"Total: {passed}/{total} tests passed")
    print("="*60)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)




