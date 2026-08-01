# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase.py
# ==========================================

import firebase_admin

from firebase_admin import credentials
from firebase_admin import db

from config import (
    FIREBASE_CREDENTIAL_PATH,
    FIREBASE_DATABASE_URL
)

# ==========================================================
# BAĞLANTI
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
# ROOT
# ==========================================================

ROOT = db.reference()

EKIPMAN_REF = ROOT.child("ekipmanlar")

SORUMLU_REF = ROOT.child("sorumlular")


# ==========================================================
# ORTAK
# ==========================================================

def _get(ref):

    data = ref.get()

    return data if data else {}


def _push(ref, value):

    yeni = ref.push()

    yeni.set(value)

    return yeni.key


def _update(ref, key, value):

    ref.child(key).update(value)


def _set(ref, key, value):

    ref.child(key).set(value)


def _pasif_yap(ref, key):

    ref.child(key).update(

        {

            "aktif": False

        }

    )


# ==========================================================
# EKİPMANLAR
# ==========================================================

def ekipmanlari_getir():

    return _get(EKIPMAN_REF)


def ekipman_ekle(data: dict):

    return _push(

        EKIPMAN_REF,

        data

    )


def ekipman_guncelle(

        firebase_key,

        data: dict

):

    _update(

        EKIPMAN_REF,

        firebase_key,

        data

    )


def ekipman_pasif_yap(firebase_key):

    _pasif_yap(

        EKIPMAN_REF,

        firebase_key

    )


# ==========================================================
# SORUMLULAR
# ==========================================================

def sorumlulari_getir():

    return _get(

        SORUMLU_REF

    )


def sorumlu_ekle(data: dict):

    return _push(

        SORUMLU_REF,

        data

    )


def sorumlu_guncelle(

        firebase_key,

        data: dict

):

    _update(

        SORUMLU_REF,

        firebase_key,

        data

    )


def sorumlu_pasif_yap(firebase_key):

    _pasif_yap(

        SORUMLU_REF,

        firebase_key

    )
