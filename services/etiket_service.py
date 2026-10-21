# ==========================================
# PERİYODİK KONTROL TAKİP
# services/etiket_service.py
# ==========================================
# Etiket fotoğrafını okuma servisine gönderir, sonucu forma hazır hale getirir.

import base64
import io

import requests

import utils
from config import (
    ETIKET_API_URL,
    ETIKET_API_TOKEN,
    ETIKET_MAX_KENAR,
    ETIKET_TIMEOUT,
)


class EtiketHatasi(Exception):
    """Kullanıcıya gösterilebilecek etiket okuma hatası."""


def _gorseli_hazirla(yol: str):
    """Fotoğrafı döndürür/küçültür ve JPEG bayt olarak verir."""

    try:
        from PIL import Image, ImageOps
    except ImportError:
        with open(yol, "rb") as f:
            return f.read()

    img = Image.open(yol)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img.thumbnail((ETIKET_MAX_KENAR, ETIKET_MAX_KENAR))

    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return buf.getvalue()


def etiket_oku(yol: str) -> dict:
    """
    Döndürür:
        {
          "ekipman_adi": str, "ekipman_id": str,
          "son_kontrol": "01.10.2026" | "", "periyot": 92 | None,
          "uyarilar": [str, ...],
        }
    """

    if not ETIKET_API_URL:
        raise EtiketHatasi("Etiket okuma servisi ayarlanmamış (config.py).")

    try:
        veri = _gorseli_hazirla(yol)
    except Exception as e:
        raise EtiketHatasi(f"Fotoğraf açılamadı: {e}")

    try:
        r = requests.post(
            ETIKET_API_URL,
            json={
                "image_base64": base64.b64encode(veri).decode("ascii"),
                "mime": "image/jpeg",
            },
            headers={"X-App-Token": ETIKET_API_TOKEN},
            timeout=ETIKET_TIMEOUT,
        )
        r.raise_for_status()
        ham = r.json()
    except requests.RequestException as e:
        raise EtiketHatasi(f"Okuma servisine ulaşılamadı: {e}")
    except ValueError:
        raise EtiketHatasi("Okuma servisinden geçersiz yanıt geldi.")

    uyarilar = []

    ad = str(ham.get("ekipman_adi") or "").strip()
    seri = str(ham.get("seri_no") or "").strip()

    if not ad:
        uyarilar.append("Ekipman adı okunamadı.")
    if not seri:
        uyarilar.append("Seri no okunamadı.")

    tarih, periyot = utils.etiket_tarihi_hesapla(
        ham.get("aylar"),
        ham.get("yil"),
    )

    if not tarih:
        uyarilar.append("Kontrol ay/yıl bilgisi okunamadı; tarihi elle girin.")

    if ham.get("notlar"):
        uyarilar.append(str(ham["notlar"]).strip())

    return {
        "ekipman_adi": ad,
        "ekipman_id": seri,
        "son_kontrol": tarih or "",
        "periyot": periyot,
        "uyarilar": uyarilar,
    }
