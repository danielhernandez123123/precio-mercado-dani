import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred_json = json.loads(os.environ["FIREBASE_CREDENTIALS"])

cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

db = firestore.client()

for user_doc in db.collection("users").list_documents():

    print("Usuario:", user_doc.id)

    products = list(
        user_doc.collection("products").stream()
    )

    for p in products:
        data = p.to_dict()

        print("\nPRODUCTO:", data.get("name"))
        print("JUMBO :", data.get("linkJumbo"))
        print("LIDER :", data.get("linkLider"))
