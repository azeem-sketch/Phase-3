import requests

url = "http://127.0.0.1:8000/api/auth/signin"
emails = ["permanet@fix.com", "azeemsaleem859@gmail.com"]
password = "password123"

for email in emails:
    print(f"Testing Signin for {email}...")
    try:
        response = requests.post(url, json={"email": email, "password": password})
        if response.status_code == 200:
            print(f"✅ {email}: SUCCESS")
        else:
            print(f"❌ {email}: FAILED ({response.status_code}) - {response.text}")
    except Exception as e:
        print(f"ERROR for {email}: {e}")
