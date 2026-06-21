import os
import json
import re
import time
import random
from datetime import datetime

import requests

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# ==========================
# FIREBASE
# ==========================

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()


# ==========================
# SCRAPER LIDER
# ==========================

def obtener_precio_lider(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0 Safari/537.36"
        )
    }

    r = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    if r.status_code != 200:
        print(f"ERROR HTTP {r.status_code}")
        return None

    html = r.text

    m = re.search(
        r'"currentPrice":\{"price":(\d+)',
        html
    )

    if not m:
        return None

    return int(m.group(1))


# ==========================
# HISTORIAL
# ==========================

def agregar_historial(history, store_id, precio):

    ahora = int(datetime.now().timestamp() * 1000)

    if store_id not in history:
        history[store_id] = []

    history[store_id].append({
        "price": precio,
        "timestamp": ahora
    })

    return history


# ==========================
# MAIN
# ==========================

print(
    "Inicio:",
    datetime.utcnow().isoformat(),
    "UTC"
)

for user_doc in db.collection("users").list_documents():

    print("\nUsuario:", user_doc.id)

    products = user_doc.collection("products").stream()

    for product in products:

        try:

            data = product.to_dict()

            nombre = data.get("name", "SIN NOMBRE")

            link_lider = data.get("linkLider")

            if not link_lider:
                print(f"{nombre}: sin link Lider")
                continue

            precio = obtener_precio_lider(link_lider)

            if precio is None:
                print(f"{nombre}: precio no encontrado")
                continue

            prices = data.get("prices", {})
            history = data.get("history", {})

            precio_anterior = prices.get("lider_cl", 0)

            if precio == precio_anterior:

                print(
                    f"{nombre}: sin cambios (${precio})"
                )

            else:

                prices["lider_cl"] = precio

                history = agregar_historial(
                    history,
                    "lider_cl",
                    precio
                )

                product.reference.update({
                    "prices": prices,
                    "history": history,
                    "updatedAt": int(
                        datetime.now().timestamp() * 1000
                    )
                })

                print(
                    f"{nombre}: "
                    f"{precio_anterior} -> {precio}"
                )

            espera = random.uniform(10, 30)

            print(
                f"Esperando {espera:.1f} s..."
            )

            time.sleep(espera)

        except Exception as e:

            print(
                f"ERROR en "
                f"{data.get('name', 'producto')}: "
                f"{e}"
            )

print("\nProceso terminado.")
