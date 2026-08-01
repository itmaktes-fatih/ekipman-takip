# ==========================================
# PERİYODİK KONTROL TAKİP
# models.py
# ==========================================

from dataclasses import dataclass
from typing import Optional

import utils


# ==========================================================
# EKİPMAN MODELİ
# ==========================================================

@dataclass
class Ekipman:

    # Firebase Anahtarı
    firebase_key: Optional[str]

    # Temel Bilgiler
    ekipman_id: str
    ekipman_adi: str

    # Kontrol Bilgileri
    son_kontrol: str
    periyot: int

    # İlişkili Sorumlu
    sorumlu_id: str

    # ------------------------------------------------------
    # HESAPLANAN ALANLAR
    # ------------------------------------------------------

    @property
    def sonraki_kontrol(self):

        return utils.sonraki_kontrol_tarihi(
            self.son_kontrol,
            self.periyot
        )

    @property
    def kalan_gun(self):

        return utils.kalan_gun(
            self.sonraki_kontrol
        )

    @property
    def durum(self):

        return utils.durum_belirle(
            self.kalan_gun
        )

    @property
    def durum_yazisi(self):

        return self.durum[0]

    @property
    def durum_ikonu(self):

        return self.durum[1]

    @property
    def durum_rengi(self):

        return self.durum[2]

    # ------------------------------------------------------
    # FIREBASE
    # ------------------------------------------------------

    def to_dict(self):

        return {

            "ekipman_id": self.ekipman_id,

            "ekipman_adi": self.ekipman_adi,

            "son_kontrol": self.son_kontrol,

            "periyot": self.periyot,

            "sorumlu_id": self.sorumlu_id

        }

    @classmethod
    def from_firebase(cls, firebase_key, data):

        return cls(

            firebase_key=firebase_key,

            ekipman_id=data.get("ekipman_id", ""),

            ekipman_adi=data.get("ekipman_adi", ""),

            son_kontrol=data.get("son_kontrol", ""),

            periyot=int(data.get("periyot", 0)),

            sorumlu_id=data.get("sorumlu_id", "")

        )


# ==========================================================
# SORUMLU MODELİ
# ==========================================================

@dataclass
class Sorumlu:

    firebase_key: Optional[str]

    ad: str

    telefon: str = ""

    email: str = ""

    aktif: bool = True

    def to_dict(self):

        return {

            "ad": self.ad,

            "telefon": self.telefon,

            "email": self.email,

            "aktif": self.aktif

        }

    @classmethod
    def from_firebase(cls, firebase_key, data):

        return cls(

            firebase_key=firebase_key,

            ad=data.get("ad", ""),

            telefon=data.get("telefon", ""),

            email=data.get("email", ""),

            aktif=data.get("aktif", True)

        )
