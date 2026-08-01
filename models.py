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

@dataclass(slots=True)
class Ekipman:
    """
    Sistemde kayıtlı ekipman modeli.
    """

    # Firebase Key
    firebase_key: Optional[str] = None

    # Temel Bilgiler
    ekipman_id: str = ""
    ekipman_adi: str = ""

    # Kontrol Bilgileri
    son_kontrol: str = ""
    periyot: int = 365

    # İlişkiler
    sorumlu_id: str = ""

    # Soft Delete
    aktif: bool = True

    # --------------------------------------------------
    # HESAPLANAN ALANLAR
    # --------------------------------------------------

    @property
    def sonraki_kontrol(self) -> str:
        return utils.sonraki_kontrol_tarihi(
            self.son_kontrol,
            self.periyot
        )

    @property
    def kalan_gun(self) -> int:
        return utils.kalan_gun(
            self.sonraki_kontrol
        )

    @property
    def durum(self):
        """
        Döndürür:

        ("Geçerli","check-circle","success")
        """

        return utils.durum_belirle(
            self.kalan_gun
        )

    @property
    def durum_yazisi(self) -> str:
        return self.durum[0]

    @property
    def durum_ikonu(self) -> str:
        return self.durum[1]

    @property
    def durum_rengi(self) -> str:
        return self.durum[2]

    @property
    def kalan_gun_yazisi(self) -> str:
        return utils.kalan_gun_yazisi(
            self.kalan_gun
        )

    # --------------------------------------------------
    # FIREBASE
    # --------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "ekipman_id": self.ekipman_id,

            "ekipman_adi": self.ekipman_adi,

            "son_kontrol": self.son_kontrol,

            "periyot": self.periyot,

            "sorumlu_id": self.sorumlu_id,

            "aktif": self.aktif

        }

    @classmethod
    def from_firebase(cls, firebase_key: str, data: dict):

        return cls(

            firebase_key=firebase_key,

            ekipman_id=data.get(
                "ekipman_id", ""
            ),

            ekipman_adi=data.get(
                "ekipman_adi", ""
            ),

            son_kontrol=data.get(
                "son_kontrol", ""
            ),

            periyot=int(
                data.get("periyot", 365)
            ),

            sorumlu_id=data.get(
                "sorumlu_id", ""
            ),

            aktif=bool(
                data.get("aktif", True)
            )

        )


# ==========================================================
# SORUMLU MODELİ
# ==========================================================

@dataclass(slots=True)
class Sorumlu:
    """
    Ekipmanlardan sorumlu kişi.
    """

    firebase_key: Optional[str] = None

    ad: str = ""

    telefon: str = ""

    email: str = ""

    aktif: bool = True

    # --------------------------------------------------

    def to_dict(self) -> dict:

        return {

            "ad": self.ad,

            "telefon": self.telefon,

            "email": self.email,

            "aktif": self.aktif

        }

    @classmethod
    def from_firebase(cls, firebase_key: str, data: dict):

        return cls(

            firebase_key=firebase_key,

            ad=data.get(
                "ad", ""
            ),

            telefon=data.get(
                "telefon", ""
            ),

            email=data.get(
                "email", ""
            ),

            aktif=bool(
                data.get("aktif", True)
            )

        )
