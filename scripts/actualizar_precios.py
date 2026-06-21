import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

users = list(db.collection("users").stream())

print("Usuarios:", len(users))

for user in users:
    print("UID =", user.id)

    products = list(
        db.collection("users")
        .document(user.id)
        .collection("products")
        .stream()
    )

    print("Productos:", len(products))

    for p in products[:5]:
        print("Producto:", p.id)
        print(p.to_dict())
