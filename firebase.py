# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase.py
# ==========================================

import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

from config import FIREBASE_CREDENTIAL_PATH, FIREBASE_DATABASE_URL


# ==========================================================
# FIREBASE BAĞLANTISI
# ==========================================================

if not firebase_admin._apps:

    cred = credentials.Certificate(
        FIREBASE_CREDENTIAL_PATH
    )

    firebase_admin.initialize_app(

        cred,

        {
            "databaseURL": FIREBASE_DATABASE_URL
        }

    )


# ==========================================================
# REFERANSLAR
# ==========================================================

ekipman_ref = db.reference("ekipmanlar")

sorumlu_ref = db.reference("sorumlular")


# ==========================================================
# EKİPMAN
# ==========================================================

def get_ekipmanlar():

    veri = ekipman_ref.get()

    return veri if veri else {}


def ekipman_ekle(ekipman):

    yeni = ekipman_ref.push()

    yeni.set(

        ekipman.to_dict()

    )

    return yeni.key


def ekipman_guncelle(firebase_key, ekipman):

    ekipman_ref.child(

        firebase_key

    ).update(

        ekipman.to_dict()

    )


def ekipman_soft_delete(firebase_key):

    ekipman_ref.child(

        firebase_key

    ).update(

        {

            "aktif": False

        }

    )


# ==========================================================
# SORUMLULAR
# ==========================================================

def get_sorumlular():

    veri = sorumlu_ref.get()

    return veri if veri else {}


def sorumlu_ekle(sorumlu):

    yeni = sorumlu_ref.push()

    yeni.set(

        sorumlu.to_dict()

    )

    return yeni.key


def sorumlu_guncelle(firebase_key, sorumlu):

    sorumlu_ref.child(

        firebase_key

    ).update(

        sorumlu.to_dict()

    )


def sorumlu_soft_delete(firebase_key):

    sorumlu_ref.child(

        firebase_key

    ).update(

        {

            "aktif": False

        }

    )
