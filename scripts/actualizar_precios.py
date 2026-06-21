from firebase_admin import firestore

db = firestore.client()

for coleccion in db.collections():
    print("Colección:", coleccion.id)
