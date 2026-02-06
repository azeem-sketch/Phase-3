import requests

url = "http://127.0.0.1:8000/api/auth/signin"
headers = {
    "Origin": "http://127.0.0.1:3000",
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "content-type"
}

print(f"Testing OPTIONS request to {url}...")
try:
    response = requests.options(url, headers=headers)
    print(f"Status: {response.status_code}")
    print("Headers:")
    for k, v in response.headers.items():
        print(f"  {k}: {v}")
    
    if "Access-Control-Allow-Origin" in response.headers:
        print("✅ CORS headers present")
    else:
        print("❌ CORS headers MISSING")
except Exception as e:
    print(f"ERROR: {e}")
