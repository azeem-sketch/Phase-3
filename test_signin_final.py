import requests

url = "http://127.0.0.1:8000/api/auth/signin"
data = {"email": "permanet@fix.com", "password": "password123"}

print(f"Testing Signin to {url} with {data['email']}...")
try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    
    if response.status_code == 200:
        print("✅ Signin SUCCESSFUL in test script")
    else:
        print("❌ Signin FAILED in test script")
except Exception as e:
    print(f"ERROR: {e}")
