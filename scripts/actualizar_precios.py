import os
import json
import re
import time
import random
import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Firebase
cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()


def obtener_precio_lider(url):
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

    if not m:
        return None

    return int(m.group(1))


for user_doc in db.collection("users").list_documents():

    products = user_doc.collection("products").stream()

    for product in products:

        data = product.to_dict()

        link = data.get("linkLider")

        if not link:
            continue

        try:

            precio = obtener_precio_lider(link)

            if precio is None:
                print("No encontrado:", data.get("name"))
                continue

            prices = data.get("prices", {})

            viejo = prices.get("lider_cl")

            prices["lider_cl"] = precio

            product.reference.update({
                "prices": prices
            })

            print(
                f'{data.get("name")} | '
                f'{viejo} -> {precio}'
            )

            time.sleep(random.uniform(5, 15))

        except Exception as e:

            print(
                f'Error en {data.get("name")}: {e}'
            )
