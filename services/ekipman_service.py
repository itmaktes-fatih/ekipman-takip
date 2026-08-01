# ==========================================
# PERİYODİK KONTROL TAKİP
# services/ekipman_service.py
# ==========================================

from models import Ekipman
import firebase


class EkipmanService:

    # ======================================================
    # TÜM EKİPMANLAR
    # ======================================================

    @staticmethod
    def tumunu_getir():

        veriler = firebase.ekipmanlari_getir()

        liste = []

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

        return liste

    # ======================================================
    # TEK EKİPMAN
    # ======================================================

    @staticmethod
    def getir(firebase_key):

        for ekipman in EkipmanService.tumunu_getir():

            if ekipman.firebase_key == firebase_key:

                return ekipman

        return None

    # ======================================================
    # EKLE
    # ======================================================

    @staticmethod
    def ekle(ekipman: Ekipman):

        if EkipmanService.id_var_mi(
                ekipman.ekipman_id):

            raise ValueError(
                "Bu ekipman ID'si zaten kayıtlı."
            )

        return firebase.ekipman_ekle(
            ekipman.to_dict()
        )

    # ======================================================
    # GÜNCELLE
    # ======================================================

    @staticmethod
    def guncelle(ekipman: Ekipman):

        firebase.ekipman_guncelle(

            ekipman.firebase_key,

            ekipman.to_dict()

        )

    # ======================================================
    # PASİF YAP
    # ======================================================

    @staticmethod
    def sil(firebase_key):

        firebase.ekipman_pasif_yap(
            firebase_key
        )

    # ======================================================
    # ID KONTROL
    # ======================================================

    @staticmethod
    def id_var_mi(ekipman_id):

        ekipman_id = ekipman_id.strip().lower()

        for ekipman in EkipmanService.tumunu_getir():

            if ekipman.ekipman_id.lower() == ekipman_id:

                return True

        return False

    # ======================================================
    # ARAMA
    # ======================================================

    @staticmethod
    def ara(metin):

        metin = metin.lower()

        sonuc = []

        for ekipman in EkipmanService.tumunu_getir():

            if (

                metin in ekipman.ekipman_adi.lower()

                or

                metin in ekipman.ekipman_id.lower()

            ):

                sonuc.append(ekipman)

        return sonuc

    # ======================================================
    # DASHBOARD
    # ======================================================

    @staticmethod
    def dashboard_verisi():

        ekipmanlar = EkipmanService.tumunu_getir()

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
