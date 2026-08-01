# ==========================================
# PERİYODİK KONTROL TAKİP
# services/sorumlu_service.py
# ==========================================

from models import Sorumlu
import firebase


class SorumluService:

    # ======================================================
    # TÜM SORUMLULAR
    # ======================================================

    @staticmethod
    def tumunu_getir():

        veriler = firebase.sorumlulari_getir()

        liste = []

        for key, value in veriler.items():

            sorumlu = Sorumlu.from_firebase(
                key,
                value
            )

            if sorumlu.aktif:
                liste.append(sorumlu)

        liste.sort(
            key=lambda x: x.ad.lower()
        )

        return liste

    # ======================================================
    # TEK KAYIT
    # ======================================================

    @staticmethod
    def getir(firebase_key):

        for sorumlu in SorumluService.tumunu_getir():

            if sorumlu.firebase_key == firebase_key:

                return sorumlu

        return None

    # ======================================================
    # EKLE
    # ======================================================

    @staticmethod
    def ekle(sorumlu: Sorumlu):

        if SorumluService.isim_var_mi(
                sorumlu.ad):

            raise ValueError(
                "Bu isimde bir sorumlu zaten mevcut."
            )

        return firebase.sorumlu_ekle(
            sorumlu.to_dict()
        )

    # ======================================================
    # GÜNCELLE
    # ======================================================

    @staticmethod
    def guncelle(sorumlu: Sorumlu):

        firebase.sorumlu_guncelle(

            sorumlu.firebase_key,

            sorumlu.to_dict()

        )

    # ======================================================
    # PASİF YAP
    # ======================================================

    @staticmethod
    def sil(firebase_key):

        firebase.sorumlu_pasif_yap(
            firebase_key
        )

    # ======================================================
    # İSİM KONTROLÜ
    # ======================================================

    @staticmethod
    def isim_var_mi(ad):

        ad = ad.strip().lower()

        for sorumlu in SorumluService.tumunu_getir():

            if sorumlu.ad.lower() == ad:

                return True

        return False

    # ======================================================
    # ARAMA
    # ======================================================

    @staticmethod
    def ara(metin):

        metin = metin.lower()

        sonuc = []

        for sorumlu in SorumluService.tumunu_getir():

            if metin in sorumlu.ad.lower():

                sonuc.append(sorumlu)

        return sonuc

    # ======================================================
    # DROPDOWN LİSTESİ
    # ======================================================

    @staticmethod
    def dropdown_listesi():

        return [

            (
                s.firebase_key,
                s.ad
            )

            for s in SorumluService.tumunu_getir()

        ]

    # ======================================================
    # ID -> AD
    # ======================================================

    @staticmethod
    def ad_getir(firebase_key):

        sorumlu = SorumluService.getir(
            firebase_key
        )

        if sorumlu:

            return sorumlu.ad

        return "-"
