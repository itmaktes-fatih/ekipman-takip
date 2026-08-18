# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase.py
# ==========================================
# Firebase Realtime Database REST API.
# Android/buildozer uyumlu olacak şekilde firebase_admin kullanılmaz.
# ==========================================

import requests

import firebase_auth

from config import (
    FIREBASE_URL,
    FIREBASE_AUTH_TOKEN,
    FIREBASE_WEB_API_KEY,
    NODE_EKIPMANLAR,
    NODE_SORUMLULAR,
)

TIMEOUT = 10


# ==========================================================
# ORTAK
# ==========================================================

def _auth_parametresi() -> str:
    """Firebase REST istekleri için kullanılacak auth token'ını döndürür."""

    if FIREBASE_AUTH_TOKEN:
        return FIREBASE_AUTH_TOKEN

    if FIREBASE_WEB_API_KEY:
        return firebase_auth.id_token()

    return ""


def _url(node, key=None):
    parca = f"{node}/{key}" if key else node
    url = f"{FIREBASE_URL.rstrip('/')}/{parca}.json"

    token = _auth_parametresi()
    if token:
        url += f"?auth={token}"

    return url


def _get(node):
    try:
        r = requests.get(_url(node), timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return data if isinstance(data, dict) else {}

    except Exception as e:
        print("Firebase GET HATASI:", type(e).__name__, str(e))
        return {}


def _push(node, value):
    try:
        r = requests.post(
            _url(node),
            json=value,
            timeout=TIMEOUT,
        )
        r.raise_for_status()

        data = r.json()
        if not isinstance(data, dict):
            return None

        return data.get("name")

    except Exception as e:
        print("Firebase PUSH HATASI:", type(e).__name__, str(e))
        return None


def _update(node, key, value):
    if not key:
        return False

    try:
        r = requests.patch(
            _url(node, key),
            json=value,
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        return True

    except Exception as e:
        print("Firebase PATCH HATASI:", type(e).__name__, str(e))
        return False


def _pasif_yap(node, key):
    return _update(node, key, {"aktif": False})


def _aktif_yap(node, key):
    return _update(node, key, {"aktif": True})


# ==========================================================
# EKİPMANLAR
# ==========================================================

def ekipmanlari_getir():
    return _get(NODE_EKIPMANLAR)


def ekipman_ekle(data: dict):
    return _push(NODE_EKIPMANLAR, data)


def ekipman_guncelle(firebase_key: str, data: dict):
    return _update(NODE_EKIPMANLAR, firebase_key, data)


def ekipman_pasif_yap(firebase_key: str):
    return _pasif_yap(NODE_EKIPMANLAR, firebase_key)


def ekipman_aktif_yap(firebase_key: str):
    return _aktif_yap(NODE_EKIPMANLAR, firebase_key)


# ==========================================================
# SORUMLULAR
# ==========================================================

def sorumlulari_getir():
    return _get(NODE_SORUMLULAR)


def sorumlu_ekle(data: dict):
    return _push(NODE_SORUMLULAR, data)


def sorumlu_guncelle(firebase_key, data: dict):
    return _update(NODE_SORUMLULAR, firebase_key, data)


def sorumlu_pasif_yap(firebase_key):
    return _pasif_yap(NODE_SORUMLULAR, firebase_key)


def sorumlu_aktif_yap(firebase_key):
    return _aktif_yap(NODE_SORUMLULAR, firebase_key)


# Eski isimlerle uyumluluk.
get_sorumlular = sorumlulari_getir
