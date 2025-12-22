import requests

# Test if the token endpoint exists
try:
    response = requests.get("http://localhost:8000/api/v1/auth/token")
    print(f"GET /api/v1/auth/token: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")

# Test POST to token endpoint
try:
    data = {
        "username": "test@example.com",
        "password": "TestPass123"
    }
    response = requests.post("http://localhost:8000/api/v1/auth/token", data=data)
    print(f"POST /api/v1/auth/token: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")