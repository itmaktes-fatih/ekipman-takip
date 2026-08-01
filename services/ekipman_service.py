# ==========================================
# PERİYODİK KONTROL TAKİP
# services/ekipman_service.py
# ==========================================

from typing import List

import firebase
import utils

from models import Ekipman


class EkipmanService:

    @staticmethod
    def tumunu_getir() -> List[Ekipman]:

        data = firebase.get_ekipmanlar()

        if not data:
            return []

        liste = []

        for firebase_key, value in data.items():

            try:

                ekipman = Ekipman.from_firebase(
                    firebase_key,
                    value
                )

                liste.append(ekipman)

            except Exception as e:

                print("Kayıt okunamadı :", e)

        liste.sort(
            key=lambda x: x.kalan_gun
        )

        return liste

    @staticmethod
    def dashboard_verisi():

        ekipmanlar = EkipmanService.tumunu_getir()

        toplam = len(ekipmanlar)

        guvenli = 0
        yaklasan = 0
        gecmis = 0

        for e in ekipmanlar:

            _, _, renk = e.durum

            if renk == "success":

                guvenli += 1

            elif renk == "warning":

                yaklasan += 1

            else:

                gecmis += 1

        return {

            "toplam": toplam,

            "guvenli": guvenli,

            "yaklasan": yaklasan,

            "gecmis": gecmis,

            "yaklasan_liste": ekipmanlar[:10]

        }

    @staticmethod
    def ekle(ekipman: Ekipman):

        return firebase.ekipman_ekle(
            ekipman.to_dict()
        )

    @staticmethod
    def guncelle(ekipman: Ekipman):

        return firebase.ekipman_guncelle(

            ekipman.firebase_key,

            ekipman.to_dict()

        )

    @staticmethod
    def sil(firebase_key):

        return firebase.ekipman_sil(firebase_key)

    @staticmethod
    def ara(kelime: str):

        kelime = kelime.lower()

        sonuc = []

        for e in EkipmanService.tumunu_getir():

            if (

                kelime in e.ekipman_adi.lower()

                or

                kelime in e.ekipman_id.lower()

                or

                kelime in e.sorumlu.lower()

            ):

                sonuc.append(e)

        return sonuc
