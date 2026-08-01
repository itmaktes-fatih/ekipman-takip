# ==========================================
# PERİYODİK KONTROL TAKİP
# services/sorumlu_service.py
# ==========================================

from typing import List

import firebase

from models import Sorumlu


class SorumluService:

    @staticmethod
    def tumunu_getir() -> List[Sorumlu]:
        """
        Firebase'den tüm sorumluları okur.
        """

        data = firebase.get_sorumlular()

        if not data:
            return []

        liste = []

        for firebase_key, value in data.items():

            try:

                sorumlu = Sorumlu.from_firebase(
                    firebase_key,
                    value
                )

                liste.append(sorumlu)

            except Exception as e:

                print("Sorumlu okunamadı :", e)

        liste.sort(
            key=lambda x: x.ad.lower()
        )

        return liste

    @staticmethod
    def isim_listesi() -> list:
        """
        Dropdown için sadece isimleri döndürür.
        """

        return [

            s.ad

            for s in SorumluService.tumunu_getir()

        ]

    @staticmethod
    def ekle(ad: str):

        ad = ad.strip()

        if ad == "":

            return False

        mevcutlar = [

            x.ad.lower()

            for x in SorumluService.tumunu_getir()

        ]

        if ad.lower() in mevcutlar:

            print("Bu sorumlu zaten kayıtlı.")

            return False

        return firebase.sorumlu_ekle(ad)

    @staticmethod
    def guncelle(sorumlu: Sorumlu):

        return firebase.sorumlu_guncelle(

            sorumlu.firebase_key,

            sorumlu.ad

        )

    @staticmethod
    def sil(firebase_key):

        return firebase.sorumlu_sil(firebase_key)

    @staticmethod
    def ara(kelime: str) -> List[Sorumlu]:

        kelime = kelime.lower()

        sonuc = []

        for s in SorumluService.tumunu_getir():

            if kelime in s.ad.lower():

                sonuc.append(s)

        return sonuc
