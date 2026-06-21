import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

print("Project ID:", cred_json["project_id"])

cred = credentials.Certificate(cred_json)

firebase_admin.initialize_app(cred)

db = firestore.client()

print("Colecciones encontradas:")

for coleccion in db.collections():
    print(" -", coleccion.id)
