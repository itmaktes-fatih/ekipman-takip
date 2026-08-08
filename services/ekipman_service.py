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

        liste = [
            Ekipman.from_firebase(key, value)
            for key, value in data.items()
            if value.get("aktif", True)
        ]

        for ekipman in liste:
            ekipman.sorumlu = EkipmanService.sorumlu_adi(ekipman)

        return liste

    @staticmethod
    def sorumlu_adi(ekipman: Ekipman) -> str:
        return SorumluService.ad_bul(ekipman.sorumlu_id)

    @staticmethod
    def ara(metin: str):

        metin = metin.lower().strip()

        return [
            e for e in EkipmanService.tumunu_getir()
            if metin in e.ekipman_adi.lower()
            or metin in e.ekipman_id.lower()
        ]

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
        return firebase.ekipman_pasif_yap(firebase_key)
