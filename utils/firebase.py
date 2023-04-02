import os

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def get_db():
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "")

    cred = credentials.Certificate(cred_path)
    app = firebase_admin.initialize_app(cred)
    db = firestore.client()

    return db
