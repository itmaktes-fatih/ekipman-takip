# ==========================================
# PERİYODİK KONTROL TAKİP
# models.py
# ==========================================

from dataclasses import dataclass
from typing import Optional

import utils


# --------------------------------------------------
# EKİPMAN MODELİ
# --------------------------------------------------

@dataclass
class Ekipman:

    firebase_key: Optional[str]

    ekipman_id: str

    ekipman_adi: str

    son_kontrol: str

    periyot: int

    sorumlu: str

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

    def to_dict(self):

        return {

            "ekipman_id": self.ekipman_id,

            "ekipman_adi": self.ekipman_adi,

            "son_kontrol": self.son_kontrol,

            "periyot": self.periyot,

            "sorumlu": self.sorumlu

        }

    @classmethod
    def from_firebase(cls, firebase_key, data):

        return cls(

            firebase_key=firebase_key,

            ekipman_id=data.get("ekipman_id", ""),

            ekipman_adi=data.get("ekipman_adi", ""),

            son_kontrol=data.get("son_kontrol", ""),

            periyot=int(data.get("periyot", 0)),

            sorumlu=data.get("sorumlu", "")

        )


# --------------------------------------------------
# SORUMLU MODELİ
# --------------------------------------------------

@dataclass
class Sorumlu:

    firebase_key: Optional[str]

    ad: str

    def to_dict(self):

        return {

            "ad": self.ad

        }

    @classmethod
    def from_firebase(cls, firebase_key, data):

        return cls(

            firebase_key=firebase_key,

            ad=data.get("ad", "")

        )
