import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

uid = "xp6AChrnInM8eMy5NCquUFX1TO02"

doc = db.collection("users").document(uid).get()

print("Existe:", doc.exists)

products = list(
    db.collection("users")
    .document(uid)
    .collection("products")
    .stream()
)

print("Cantidad de productos:", len(products))

for p in products[:10]:
    print("\nID:", p.id)
    print(p.to_dict())
