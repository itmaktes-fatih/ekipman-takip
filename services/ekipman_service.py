# ==========================================
# PERİYODİK KONTROL TAKİP
# services/ekipman_service.py
# ==========================================

import firebase

from models import Ekipman
from services.cache import Cache
from services.sorumlu_service import SorumluService


class EkipmanService:

    # =====================================================
    # TÜM EKİPMANLARI GETİR
    # =====================================================

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

    # =====================================================
    # FIREBASE KEY İLE GETİR
    # =====================================================

    @classmethod
    def getir(cls, firebase_key):

        for ekipman in cls.tumunu_getir():

            if ekipman.firebase_key == firebase_key:
                return ekipman

        return None

    # =====================================================
    # EKİPMAN ID İLE GETİR
    # =====================================================

    @classmethod
    def id_ile_getir(cls, ekipman_id):

        ekipman_id = ekipman_id.strip().lower()

        for ekipman in cls.tumunu_getir():

            if ekipman.ekipman_id.lower() == ekipman_id:
                return ekipman

        return None

    # =====================================================
    # EKLE
    # =====================================================

    @classmethod
    def ekle(cls, ekipman: Ekipman):

        if cls.id_var_mi(ekipman.ekipman_id):

            raise ValueError(
                "Bu ekipman ID'si zaten kayıtlı."
            )

        firebase_key = firebase.ekipman_ekle(
            ekipman.to_dict()
        )

        Cache.temizle()

        return firebase_key

    # =====================================================
    # GÜNCELLE
    # =====================================================

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

    # =====================================================
    # PASİF YAP (SOFT DELETE)
    # =====================================================

    @classmethod
    def sil(cls, firebase_key):

        firebase.ekipman_pasif_yap(
            firebase_key
        )

        Cache.temizle()

    # =====================================================
    # ID KONTROL
    # =====================================================

    @classmethod
    def id_var_mi(cls, ekipman_id):

        return cls.id_ile_getir(
            ekipman_id
        ) is not None

    # =====================================================
    # ARAMA
    # =====================================================

    @classmethod
    def ara(cls, aranan):

        aranan = aranan.strip().lower()

        sonuc = []

        for ekipman in cls.tumunu_getir():

            sorumlu = SorumluService.ad_getir(
                ekipman.sorumlu_id
            ).lower()

            if (

                aranan in ekipman.ekipman_adi.lower()

                or

                aranan in ekipman.ekipman_id.lower()

                or

                aranan in sorumlu

            ):

                sonuc.append(ekipman)

        return sonuc

    # =====================================================
    # DURUMA GÖRE FİLTRELE
    # =====================================================

    @classmethod
    def filtrele(cls, durum_rengi):

        return [

            ekipman

            for ekipman in cls.tumunu_getir()

            if ekipman.durum_rengi == durum_rengi

        ]

    # =====================================================
    # YAKLAŞAN KONTROLLER
    # =====================================================

    @classmethod
    def yaklasan_kontroller(cls, gun=30):

        sonuc = []

        for ekipman in cls.tumunu_getir():

            if 0 <= ekipman.kalan_gun <= gun:

                sonuc.append(ekipman)

        sonuc.sort(
            key=lambda x: x.kalan_gun
        )

        return sonuc

    # =====================================================
    # SÜRESİ GEÇENLER
    # =====================================================

    @classmethod
    def suresi_gecenler(cls):

        sonuc = [

            ekipman

            for ekipman in cls.tumunu_getir()

            if ekipman.kalan_gun < 0

        ]

        sonuc.sort(
            key=lambda x: x.kalan_gun
        )

        return sonuc

    # =====================================================
    # DASHBOARD
    # =====================================================

    @classmethod
    def dashboard_verisi(cls):

        ekipmanlar = cls.tumunu_getir()

        veri = {

            "toplam": len(ekipmanlar),

            "guvenli": 0,

            "yaklasan": 0,

            "gecmis": 0

        }

        for ekipman in ekipmanlar:

            if ekipman.durum_rengi == "success":

                veri["guvenli"] += 1

            elif ekipman.durum_rengi == "warning":

                veri["yaklasan"] += 1

            else:

                veri["gecmis"] += 1

        return veri

    # =====================================================
    # SORUMLU ADI
    # =====================================================

    @classmethod
    def sorumlu_adi(cls, ekipman):

        return SorumluService.ad_getir(
            ekipman.sorumlu_id
        )
