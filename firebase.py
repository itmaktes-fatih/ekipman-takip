# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase.py
# ==========================================

import requests

from config import (
    FIREBASE_URL,
    NODE_EKIPMANLAR,
    NODE_SORUMLULAR
)


# --------------------------------------------------
# ORTAK URL
# --------------------------------------------------

def _url(node: str) -> str:
    """
    Firebase node adresini oluşturur.
    """

    return f"{FIREBASE_URL}{node}.json"


def _item_url(node: str, key: str) -> str:
    """
    Firebase kayıt adresini oluşturur.
    """

    return f"{FIREBASE_URL}{node}/{key}.json"


# --------------------------------------------------
# EKİPMANLAR
# --------------------------------------------------

def get_ekipmanlar():

    try:

        response = requests.get(
            _url(NODE_EKIPMANLAR),
            timeout=10
        )

        response.raise_for_status()

        return response.json() or {}

    except Exception as e:

        print("Firebase Hatası :", e)

        return {}


def ekipman_ekle(veri: dict):

    try:

        response = requests.post(
            _url(NODE_EKIPMANLAR),
            json=veri,
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False


def ekipman_guncelle(key: str, veri: dict):

    try:

        response = requests.patch(
            _item_url(NODE_EKIPMANLAR, key),
            json=veri,
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False


def ekipman_sil(key: str):

    try:

        response = requests.delete(
            _item_url(NODE_EKIPMANLAR, key),
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False


# --------------------------------------------------
# SORUMLULAR
# --------------------------------------------------

def get_sorumlular():

    try:

        response = requests.get(
            _url(NODE_SORUMLULAR),
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return {}

        return data

    except Exception as e:

        print("Firebase Hatası :", e)

        return {}


def sorumlu_ekle(ad: str):

    try:

        response = requests.post(
            _url(NODE_SORUMLULAR),
            json={
                "ad": ad
            },
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False


def sorumlu_guncelle(key: str, ad: str):

    try:

        response = requests.patch(
            _item_url(NODE_SORUMLULAR, key),
            json={
                "ad": ad
            },
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False


def sorumlu_sil(key: str):

    try:

        response = requests.delete(
            _item_url(NODE_SORUMLULAR, key),
            timeout=10
        )

        response.raise_for_status()

        return True

    except Exception as e:

        print("Firebase Hatası :", e)

        return False
