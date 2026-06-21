import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()

print("Conectado a Firebase")

usuarios = list(db.collection("users").stream())

print(f"Usuarios encontrados: {len(usuarios)}")

for usuario in usuarios:
    print("UID:", usuario.id)
