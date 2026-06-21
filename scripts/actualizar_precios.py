import requests
import re

url = "https://www.jumbo.cl/chocolate-trencito-150-g-barra/p"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0 Safari/537.36"
    )
}

r = requests.get(url, headers=headers, timeout=30)

print("STATUS:", r.status_code)

html = r.text

patrones = [
    "price",
    "Price",
    "currentPrice",
    "salePrice",
    "offerPrice",
    "product-price",
    "00780223007002",
    "Trencito"
]

for patron in patrones:
    print("\n===================")
    print("BUSCANDO:", patron)

    idx = html.find(patron)

    if idx != -1:
        inicio = max(0, idx - 200)
        fin = min(len(html), idx + 500)

        print(html[inicio:fin])
    else:
        print("NO ENCONTRADO")
