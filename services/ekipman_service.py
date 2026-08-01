# ==========================================
# PERİYODİK KONTROL TAKİP
# services/ekipman_service.py
# ==========================================

import firebase

from models import Ekipman
from services.cache import Cache
from services.sorumlu_service import SorumluService


class EkipmanService:

    # ======================================================
    # TÜM EKİPMANLAR
    # ======================================================

    @classmethod
    def tumunu_getir(cls, force_refresh=False):

        if Cache.ekipmanlar is not None and not force_refresh:
            return Cache.ekipmanlar

        veriler = firebase.ekipmanlari_getir()

        liste = []

        if veriler:

            for key, value in veriler.items():

                ekipman = Ekipman.from_firebase(
                    key,
                    value
                )

                if ekipman.aktif:
                    liste.append(ekipman)

        liste.sort(
            key=lambda x: x.ekipman_adi.lower()
        )

        Cache.ekipmanlar = liste

        return liste

    # ======================================================

    @classmethod
    def getir(cls, firebase_key):

        for ekipman in cls.tumunu_getir():

            if ekipman.firebase_key == firebase_key:
                return ekipman

        return None

    # ======================================================

    @classmethod
    def ekle(cls, ekipman: Ekipman):

        if cls.id_var_mi(ekipman.ekipman_id):

            raise ValueError(
                "Bu ekipman ID'si zaten kayıtlı."
            )

        key = firebase.ekipman_ekle(
            ekipman.to_dict()
        )

        Cache.temizle()

        return key

    # ======================================================

    @classmethod
    def guncelle(cls, ekipman: Ekipman):

        for kayit in cls.tumunu_getir():

            if kayit.firebase_key == ekipman.firebase_key:
                continue

            if kayit.ekipman_id.lower() == ekipman.ekipman_id.lower():

                raise ValueError(
                    "Bu ekipman ID'si başka bir kayıt tarafından kullanılıyor."
                )

        firebase.ekipman_guncelle(

            ekipman.firebase_key,

            ekipman.to_dict()

        )

        Cache.temizle()

    # ======================================================

    @classmethod
    def sil(cls, firebase_key):

        firebase.ekipman_pasif_yap(
            firebase_key
        )

        Cache.temizle()

    # ======================================================

    @classmethod
    def id_var_mi(cls, ekipman_id):

        ekipman_id = ekipman_id.strip().lower()

        for ekipman in cls.tumunu_getir():

            if ekipman.ekipman_id.lower() == ekipman_id:
                return True

        return False

    # ======================================================

    @classmethod
    def ara(cls, metin):

        metin = metin.lower().strip()

        sonuc = []

        for ekipman in cls.tumunu_getir():

            sorumlu = SorumluService.ad_getir(
                ekipman.sorumlu_id
            ).lower()

            if (
                metin in ekipman.ekipman_adi.lower()
                or
                metin in ekipman.ekipman_id.lower()
                or
                metin in sorumlu
            ):

                sonuc.append(ekipman)

        return sonuc

    # ======================================================

    @classmethod
    def filtrele(cls, durum):

        return [

            ekipman

            for ekipman in cls.tumunu_getir()

            if ekipman.durum_rengi == durum

        ]

    # ======================================================

    @classmethod
    def dashboard_verisi(cls):

        ekipmanlar = cls.tumunu_getir()

        veri = {

            "toplam": len(ekipmanlar),

            "guvenli": 0,

            "yaklasan": 0,

            "gecmis": 0,

            "yaklasan_liste": []

        }

        for ekipman in ekipmanlar:

            if ekipman.durum_rengi == "success":

                veri["guvenli"] += 1

            elif ekipman.durum_rengi == "warning":

                veri["yaklasan"] += 1
                veri["yaklasan_liste"].append(
                    ekipman
                )

            else:

                veri["gecmis"] += 1

        veri["yaklasan_liste"].sort(
            key=lambda x: x.kalan_gun
        )

        return veri

    # ======================================================

    @classmethod
    def sorumlu_adi(cls, ekipman):

        return SorumluService.ad_getir(
            ekipman.sorumlu_id
        )
