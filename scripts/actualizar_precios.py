import requests
import re

url = "https://super.lider.cl/ip/variedad/00780223007002"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

html = requests.get(
    url,
    headers=headers,
    timeout=30
).text

m = re.search(
    r'"currentPrice":\{"price":(\d+)',
    html
)

if m:
    print("PRECIO ENCONTRADO:", int(m.group(1)))
else:
    print("NO ENCONTRADO")
