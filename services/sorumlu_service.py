# ==========================================
# PERİYODİK KONTROL TAKİP
# services/sorumlu_service.py
# ==========================================

import firebase
from models import Sorumlu


class SorumluService:

    @staticmethod
    def tumunu_getir():

        data = firebase.sorumlulari_getir()

        return [
            Sorumlu.from_firebase(key, value)
            for key, value in data.items()
            if value.get("aktif", True)
        ]

    @staticmethod
    def ad_bul(sorumlu_id: str) -> str:

        data = firebase.sorumlulari_getir()
        kayit = data.get(sorumlu_id)

        return kayit.get("ad", "-") if kayit else "-"

    @staticmethod
    def id_bul(ad: str) -> str:

        data = firebase.sorumlulari_getir()

        for key, value in data.items():
            if value.get("ad") == ad:
                return key

        return ""

    @staticmethod
    def ekle(sorumlu: Sorumlu):
        return firebase.sorumlu_ekle(sorumlu.to_dict())
