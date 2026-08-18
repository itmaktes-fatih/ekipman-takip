# ==========================================
# PERİYODİK KONTROL TAKİP
# firebase_auth.py
#
# Realtime Database "locked mode" (auth != null) kurallarıyla
# çalıştığı için, istekler öncesinde anonim bir Firebase Auth
# oturumu açıp idToken alınır. Token bellekte tutulur ve süresi
# dolmadan önce refreshToken ile otomatik yenilenir.
# ==========================================

import time
import requests

from config import FIREBASE_WEB_API_KEY

TIMEOUT = 10

SIGNUP_URL = (
    "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
    f"?key={FIREBASE_WEB_API_KEY}"
)

REFRESH_URL = (
    "https://securetoken.googleapis.com/v1/token"
    f"?key={FIREBASE_WEB_API_KEY}"
)

_state = {
    "id_token": None,
    "refresh_token": None,
    "expires_at": 0,
}


def _anonim_giris():

    r = requests.post(
        SIGNUP_URL,
        json={"returnSecureToken": True},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()

    _state["id_token"] = data["idToken"]
    _state["refresh_token"] = data["refreshToken"]
    _state["expires_at"] = time.time() + int(data["expiresIn"]) - 60

    return _state["id_token"]


def _token_yenile():

    r = requests.post(
        REFRESH_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": _state["refresh_token"],
        },
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()

    _state["id_token"] = data["id_token"]
    _state["refresh_token"] = data["refresh_token"]
    _state["expires_at"] = time.time() + int(data["expires_in"]) - 60

    return _state["id_token"]


def id_token() -> str:
    """
    Geçerli bir Firebase idToken döndürür. Gerekirse yeni oturum
    açar veya mevcut oturumu yeniler.
    """

    if not FIREBASE_WEB_API_KEY:
        return ""

    try:
        if not _state["id_token"]:
            return _anonim_giris()

        if time.time() >= _state["expires_at"]:
            return _token_yenile()

        return _state["id_token"]

    except requests.RequestException:
        return _state["id_token"] or ""