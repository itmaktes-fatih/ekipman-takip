# ==========================================
# PERİYODİK KONTROL TAKİP
# services/ekipman_service.py
# ==========================================

import firebase

from models import Ekipman
from config import MAX_WARNING_LIST
from services.sorumlu_service import SorumluService


class EkipmanService:

    # --------------------------------------------------
    # OKUMA
    # --------------------------------------------------

    @staticmethod
    def tumunu_getir():
        data = firebase.ekipmanlari_getir()

        if not isinstance(data, dict):
            return []

        liste = []

        for key, value in data.items():
            if not isinstance(value, dict):
                continue

            if not value.get("aktif", True):
                continue

            try:
                ekipman = Ekipman.from_firebase(key, value)
            except (TypeError, ValueError) as e:
                print("Geçersiz ekipman kaydı:", key, e)
                continue

            ekipman.sorumlu = EkipmanService.sorumlu_adi(ekipman)
            liste.append(ekipman)

        return liste

    @staticmethod
    def sorumlu_adi(ekipman: Ekipman) -> str:
        return SorumluService.ad_bul(ekipman.sorumlu_id)

    @staticmethod
    def ara(metin: str):
        metin = (metin or "").lower().strip()

        if not metin:
            return EkipmanService.tumunu_getir()

        return [
            e
            for e in EkipmanService.tumunu_getir()
            if metin in e.ekipman_adi.lower()
            or metin in e.ekipman_id.lower()
            or metin in e.sorumlu.lower()
        ]

    @staticmethod
    def ekipman_id_kullaniliyor(ekipman_id: str, haric_key: str = None) -> bool:
        """Aktif ekipmanlarda ID'nin daha önce kullanılıp kullanılmadığını kontrol eder."""

        hedef = (ekipman_id or "").strip().casefold()
        if not hedef:
            return False

        data = firebase.ekipmanlari_getir()
        if not isinstance(data, dict):
            return False

        for key, value in data.items():
            if key == haric_key:
                continue

            if not isinstance(value, dict):
                continue

            if not value.get("aktif", True):
                continue

            mevcut = str(value.get("ekipman_id", "")).strip().casefold()
            if mevcut == hedef:
                return True

        return False

    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    @staticmethod
    def dashboard_verisi() -> dict:
        liste = EkipmanService.tumunu_getir()

        guvenli = [e for e in liste if e.durum_rengi == "success"]
        yaklasan = [e for e in liste if e.durum_rengi == "warning"]
        gecmis = [e for e in liste if e.durum_rengi == "error"]

        yaklasan_liste = sorted(
            yaklasan + gecmis,
            key=lambda e: e.kalan_gun,
        )[:MAX_WARNING_LIST]

        return {
            "toplam": len(liste),
            "guvenli": len(guvenli),
            "yaklasan": len(yaklasan),
            "gecmis": len(gecmis),
            "yaklasan_liste": yaklasan_liste,
        }

    # --------------------------------------------------
    # YAZMA
    # --------------------------------------------------

    @staticmethod
    def ekle(veri: dict):
        return firebase.ekipman_ekle(veri)

    @staticmethod
    def guncelle(firebase_key: str, veri: dict):
        return firebase.ekipman_guncelle(firebase_key, veri)

    @staticmethod
    def sil(firebase_key: str):
        """Fiziksel silme yapmaz; ekipmanı pasife alır."""
        return firebase.ekipman_pasif_yap(firebase_key)

    @staticmethod
    def aktiflestir(firebase_key: str):
        return firebase.ekipman_aktif_yap(firebase_key)
