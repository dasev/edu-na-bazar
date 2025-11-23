import requests
import json

# Test error handling
print("Testing /test-error...")
try:
    response = requests.get("http://localhost:8000/test-error")
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
    print(f"Response text: {response.text[:1000]}")

# Test 404
print("\n\nTesting 404...")
try:
    response = requests.get("http://localhost:8000/api/nonexistent")
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")

# Test validation error
print("\n\nTesting validation error...")
try:
    response = requests.post("http://localhost:8000/api/categories", json={"name": ""})
    print(f"Status: {response.status_code}")
    print("Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
