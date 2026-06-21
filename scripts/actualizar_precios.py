import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

print("Buscando documentos en users...")

docs = db.collection("users").list_documents()

count = 0

for d in docs:
    count += 1
    print("Documento encontrado:", d.id)

print("Total:", count)
