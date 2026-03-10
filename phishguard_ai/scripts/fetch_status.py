import requests

if __name__ == "__main__":
    r = requests.get("http://127.0.0.1:8000/api-status/")
    print("status:", r.status_code)
    print(r.text)
