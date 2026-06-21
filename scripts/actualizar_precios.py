import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection("users")

docs = list(users_ref.limit(20).stream())

print("Cantidad de documentos:", len(docs))

for doc in docs:
    print("Documento:", doc.id)
    print(doc.to_dict())
