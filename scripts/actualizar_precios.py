import os
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

db = firestore.client()

for coleccion in db.collections():
    print("Colección:", coleccion.id)
