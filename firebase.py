# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase.py
#
# NOT: Orijinal dosyada firebase_admin (sunucu SDK'sı) kullanılıyordu.
# Bu, Android/buildozer ortamında ÇALIŞMAZ ve servis hesabı JSON
# anahtarını telefona gömmeyi gerektirirdi (güvenlik riski).
# Bunun yerine buildozer.spec'te zaten bulunan "requests" kütüphanesi
# ile Firebase Realtime Database REST API kullanılıyor.
# ==========================================

import requests

from config import (
    FIREBASE_URL,
    FIREBASE_AUTH_TOKEN,
    NODE_EKIPMANLAR,
    NODE_SORUMLULAR,
)

TIMEOUT = 10


# ==========================================================
# ORTAK
# ==========================================================

def _url(node, key=None):

    parca = f"{node}/{key}" if key else node

    url = f"{FIREBASE_URL.rstrip('/')}/{parca}.json"

    if FIREBASE_AUTH_TOKEN:
        url += f"?auth={FIREBASE_AUTH_TOKEN}"

    return url


def _get(node):

    try:
        r = requests.get(_url(node), timeout=TIMEOUT)
        r.raise_for_status()
        data = r.json()
        return data if data else {}

    except requests.RequestException:
        return {}


def _push(node, value):

    try:
        r = requests.post(_url(node), json=value, timeout=TIMEOUT)
        r.raise_for_status()
        return r.json().get("name")

    except requests.RequestException:
        return None


def _update(node, key, value):

    try:
        r = requests.patch(_url(node, key), json=value, timeout=TIMEOUT)
        r.raise_for_status()
        return True

    except requests.RequestException:
        return False


def _pasif_yap(node, key):

    return _update(node, key, {"aktif": False})


# ==========================================================
# EKİPMANLAR
# ==========================================================

def ekipmanlari_getir():
    return _get(NODE_EKIPMANLAR)


def ekipman_ekle(data: dict):
    return _push(NODE_EKIPMANLAR, data)


def ekipman_guncelle(firebase_key, data: dict):
    return _update(NODE_EKIPMANLAR, firebase_key, data)


def ekipman_pasif_yap(firebase_key):
    return _pasif_yap(NODE_EKIPMANLAR, firebase_key)


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


# Eski isimlerle uyumluluk (form ekranı bu isimlerle çağırıyordu)
get_sorumlular = sorumlulari_getir
