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


# ==========================================
# FIREBASE
# ==========================================

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()


# ==========================================
# HEADERS
# ==========================================

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "es-CL,es;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Connection": "keep-alive"
}


# ==========================================
# SCRAPER LIDER
# ==========================================

def obtener_precio_lider(url):

    try:

        html = requests.get(
            url,
            headers=HEADERS,
            timeout=30
        ).text

        m = re.search(
            r'"currentPrice":\{"price":(\d+)',
            html
        )

        if not m:
            return None

        return int(m.group(1))

    except Exception as e:

        print("Error Líder:", e)
        return None


# ==========================================
# SCRAPER JUMBO
# ==========================================
def obtener_precio_jumbo(url):

    for intento in range(1, 4):

        try:

            print(f"Consultando Jumbo (intento {intento}/3): {url}")

            response = requests.get(
                url,
                headers=HEADERS,
                timeout=30
            )

            html = response.text

            # Método 1 (meta tag)
            m = re.search(
                r'product:price:amount[^>]*content="(\d+)"',
                html
            )

            if m:
                precio = int(m.group(1))
                print(f"Jumbo método 1: {precio}")
                return precio

            # Método 2 (JSON VTEX)
            m = re.search(
                r'"price":(\d+),"listPrice"',
                html
            )

            if m:
                precio = int(m.group(1))
                print(f"Jumbo método 2: {precio}")
                return precio

            # Método 3 (genérico)
            m = re.search(
                r'"price"\s*:\s*(\d+)',
                html
            )

            if m:
                precio = int(m.group(1))
                print(f"Jumbo método 3: {precio}")
                return precio

            print(f"No se encontró precio (intento {intento})")

        except Exception as e:

            print(f"Error Jumbo intento {intento}: {e}")

        # Esperar antes de reintentar
        if intento < 3:

            espera = random.uniform(60, 80)

            print(
                f"Reintentando en {espera:.1f} segundos..."
            )

            time.sleep(espera)

    print("NO SE ENCONTRÓ PRECIO EN JUMBO")
    print(url)

    return None
# ==========================================
# HISTORIAL
# ==========================================

def agregar_historial(history, store_id, precio):

    ahora = int(datetime.now().timestamp() * 1000)

    if store_id not in history:
        history[store_id] = []

    history[store_id].append({
        "price": precio,
        "date": ahora
    })

    return history


# ==========================================
# MAIN
# ==========================================

print("\n===================================")
print("INICIO:", datetime.utcnow().isoformat(), "UTC")
print("===================================\n")

for user_doc in db.collection("users").list_documents():

    print(f"\nUsuario: {user_doc.id}")

    productos = user_doc.collection("products").stream()

    for product in productos:

        try:

            data = product.to_dict()

            nombre = data.get("name", "Sin nombre")

            print(f"\n--- {nombre} ---")

            prices = data.get("prices", {})
            history = data.get("history", {})

            hubo_cambios = False

            # =====================================
            # LIDER.CL
            # =====================================

            link_lider = data.get("linkLider", "").strip()

            if link_lider:

                precio_lider = obtener_precio_lider(link_lider)

                if precio_lider is not None:

                    viejo = prices.get("lider_cl", 0)

                    if viejo != precio_lider:

                        print(
                            f"Lider.cl: {viejo} -> {precio_lider}"
                        )

                        prices["lider_cl"] = precio_lider

                        history = agregar_historial(
                            history,
                            "lider_cl",
                            precio_lider
                        )

                        hubo_cambios = True

                    else:

                        print(
                            f"Lider.cl sin cambios (${precio_lider})"
                        )

                else:

                    print("No se pudo obtener precio Lider.cl")

            # =====================================
            # JUMBO.CL
            # =====================================

            link_jumbo = data.get("linkJumbo", "").strip()

            if link_jumbo:

                precio_jumbo = obtener_precio_jumbo(link_jumbo)

                if precio_jumbo is not None:

                    viejo = prices.get("jumbo_cl", 0)

                    if viejo != precio_jumbo:

                        print(
                            f"Jumbo.cl: {viejo} -> {precio_jumbo}"
                        )

                        prices["jumbo_cl"] = precio_jumbo

                        history = agregar_historial(
                            history,
                            "jumbo_cl",
                            precio_jumbo
                        )

                        hubo_cambios = True

                    else:

                        print(
                            f"Jumbo.cl sin cambios (${precio_jumbo})"
                        )

                else:

                    print("No se pudo obtener precio Jumbo.cl")

            # =====================================
            # FIRESTORE
            # =====================================

            if hubo_cambios:

                product.reference.update({
                    "prices": prices,
                    "history": history,
                    "updatedAt": int(
                        datetime.now().timestamp() * 1000
                    )
                })

                print("Firestore actualizado")

            else:

                print("Sin cambios")

            espera = random.uniform(20, 60)

            print(
                f"Esperando {espera:.1f} segundos..."
            )

            time.sleep(espera)

        except Exception as e:

            print(
                f"ERROR en {data.get('name', 'producto')}: {e}"
            )

print("\n===================================")
print("PROCESO TERMINADO")
print("===================================")
