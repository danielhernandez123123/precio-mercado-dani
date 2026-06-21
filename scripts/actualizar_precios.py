import requests

url = "https://super.lider.cl/ip/variedad/00780223007002"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)

print("\nPRIMEROS 1000 CARACTERES:\n")
print(r.text[:1000])
